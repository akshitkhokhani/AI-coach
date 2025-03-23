import faiss
import numpy as np
import pandas as pd
import logging
import uuid
from typing import List, Dict, Any, Union
from app.services.embedding import EmbeddingService
from app.config import (
    VECTOR_DB_TYPE, 
    TOP_K_RESULTS, 
    PINECONE_API_KEY,
    PINECONE_INDEX_NAME,
    PINECONE_NAMESPACE,
    PINECONE_DIMENSION,
    PINECONE_METRIC
)

logger = logging.getLogger(__name__)

class VectorDBService:
    """Service for storing and retrieving vector embeddings"""
    
    def __init__(self, embedding_service: EmbeddingService = None):
        self.embedding_service = embedding_service or EmbeddingService()
        self.db_type = VECTOR_DB_TYPE
        
        if self.db_type == "faiss":
            self.index = None
            self.metadata = []  # Store metadata associated with each vector
        elif self.db_type == "pinecone":
            if not PINECONE_API_KEY:
                raise ValueError("PINECONE_API_KEY environment variable is required for Pinecone")
            self._init_pinecone()
        else:
            raise ValueError(f"Unsupported vector database type: {self.db_type}")
    
    def _init_pinecone(self):
        """Initialize connection to Pinecone"""
        try:
            # Import Pinecone
            from pinecone import Pinecone
            
            # Initialize Pinecone client with the new API
            pc = Pinecone(api_key=PINECONE_API_KEY)
            
            # Check if the index exists
            index_list = [idx.name for idx in pc.list_indexes()]
            
            if PINECONE_INDEX_NAME not in index_list:
                logger.warning(f"Index {PINECONE_INDEX_NAME} does not exist. Please create it manually in the Pinecone console.")
                logger.warning(f"Required settings: dimension={PINECONE_DIMENSION}, metric={PINECONE_METRIC}")
                raise ValueError(f"Index {PINECONE_INDEX_NAME} does not exist")
            
            # Connect to the index
            self.index = pc.Index(PINECONE_INDEX_NAME)
            logger.info(f"Connected to Pinecone index: {PINECONE_INDEX_NAME}")
        except Exception as e:
            logger.error(f"Failed to initialize Pinecone: {str(e)}")
            raise
    
    def create_index(self, dimension):
        """Create a new index"""
        if self.db_type == "faiss":
            self.index = faiss.IndexFlatL2(dimension)
            self.metadata = []
            logger.info(f"Created new FAISS index with dimension {dimension}")
        elif self.db_type == "pinecone":
            # Index is created in _init_pinecone() if it doesn't exist
            pass
    
    def load_data(self, data_source):
        """
        Load data from CSV file or DataFrame, generate embeddings, and build index
        
        Args:
            data_source (str or pandas.DataFrame): Path to CSV file or DataFrame containing context and response columns
            
        Returns:
            int: Number of records loaded
        """
        # Load dataset if string path is provided
        if isinstance(data_source, str):
            logger.info(f"Loading dataset from {data_source}")
            df = pd.read_csv(data_source)
        else:
            # Assume it's already a DataFrame
            df = data_source
        
        if 'Context' not in df.columns or 'Response' not in df.columns:
            raise ValueError("Dataset must contain 'Context' and 'Response' columns")
        
        # Generate embeddings for contexts
        contexts = df['Context'].tolist()
        logger.info(f"Generating embeddings for {len(contexts)} contexts")
        embeddings = self.embedding_service.get_embeddings(contexts)
        
        if self.db_type == "faiss":
            # Create index with appropriate dimensions if it doesn't exist
            if self.index is None:
                self.create_index(embeddings.shape[1])
                
            # Add vectors to index
            self.index.add(np.array(embeddings).astype('float32'))
            
            # Store metadata
            self.metadata.extend(df.to_dict('records'))
            
            logger.info(f"Successfully loaded {len(df)} records into FAISS vector database")
            return len(df)
        
        elif self.db_type == "pinecone":
            # Prepare vectors for Pinecone using the new format
            vectors_to_upsert = []
            for i, (_, row) in enumerate(df.iterrows()):
                vectors_to_upsert.append({
                    "id": str(uuid.uuid4()),
                    "values": embeddings[i].tolist(),
                    "metadata": {
                        'Context': row['Context'],
                        'Response': row['Response']
                    }
                })
            
            # Upsert to Pinecone
            try:
                self.index.upsert(
                    vectors=vectors_to_upsert,
                    namespace=PINECONE_NAMESPACE
                )
                logger.info(f"Successfully loaded {len(vectors_to_upsert)} records into Pinecone vector database")
                return len(vectors_to_upsert)
            except Exception as e:
                logger.error(f"Error upserting vectors to Pinecone: {str(e)}")
                raise
    
    def search(self, query, k=TOP_K_RESULTS):
        """
        Perform similarity search
        
        Args:
            query (str): Query text
            k (int): Number of top results to return
            
        Returns:
            list: List of dictionaries containing similar items and their metadata
        """
        # Generate embedding for query
        query_embedding = self.embedding_service.get_embeddings(query)
        
        if self.db_type == "faiss":
            if self.index is None:
                raise ValueError("FAISS index not initialized. Load data first.")
                
            # Ensure the embedding is 2D
            if len(query_embedding.shape) == 1:
                query_embedding = query_embedding.reshape(1, -1)
            
            # Perform search
            distances, indices = self.index.search(query_embedding.astype('float32'), k)
            
            # Format results
            results = []
            for i, idx in enumerate(indices[0]):
                if idx < len(self.metadata):  # Ensure index is valid
                    result = self.metadata[idx].copy()
                    result['similarity_score'] = float(1 / (1 + distances[0][i]))  # Convert distance to similarity score
                    results.append(result)
            
        elif self.db_type == "pinecone":
            # Perform search in Pinecone using the new API
            search_results = self.index.query(
                namespace=PINECONE_NAMESPACE,
                vector=query_embedding.tolist() if len(query_embedding.shape) == 1 else query_embedding[0].tolist(),
                top_k=k,
                include_values=True,
                include_metadata=True
            )
            
            # Format results
            results = []
            for match in search_results.matches:
                result = {
                    'Context': match.metadata['Context'],
                    'Response': match.metadata['Response'],
                    'similarity_score': match.score
                }
            
                results.append(result)
        
        logger.info(f"Found {len(results)} similar examples for query")
        return results