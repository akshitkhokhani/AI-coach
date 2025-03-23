import numpy as np
from sentence_transformers import SentenceTransformer
import logging
from tqdm import tqdm
from app.config import EMBEDDING_MODEL, EMBEDDING_MODEL_SOURCE, PINECONE_API_KEY

logger = logging.getLogger(__name__)

class EmbeddingService:
    """Service for generating text embeddings"""
    
    def __init__(self, model_name=EMBEDDING_MODEL, model_source=EMBEDDING_MODEL_SOURCE):
        self.model_name = model_name
        self.model_source = model_source
        
        if self.model_source == "sentence-transformers":
            self.model = SentenceTransformer(model_name)
        elif self.model_source == "openai":
            import openai
            from app.config import OPENAI_API_KEY
            openai.api_key = OPENAI_API_KEY
            self.model = None  # OpenAI doesn't need a local model
        elif self.model_source == "pinecone":
            # Setup for Pinecone hosted models
            from pinecone import Pinecone
            try:
                self.pc = Pinecone(api_key=PINECONE_API_KEY)
                logger.info(f"Successfully initialized Pinecone client for embeddings")
            except Exception as e:
                logger.error(f"Failed to initialize Pinecone client for embeddings: {str(e)}")
                self.pc = None
            self.model = None
    
    def get_embeddings(self, texts):
        """
        Generate embeddings for a list of texts
        
        Args:
            texts (list or str): Text string or list of text strings
            
        Returns:
            numpy.ndarray: Array of embeddings
        """
        if isinstance(texts, str):
            texts = [texts]
        
        if self.model_source == "sentence-transformers":
            embeddings = self.model.encode(texts)
            return embeddings
        elif self.model_source == "openai":
            import openai
            # Use OpenAI embeddings API
            response = openai.embeddings.create(
                input=texts,
                model="text-embedding-3-small"
            )
            embeddings = np.array([item.embedding for item in response.data])
            return embeddings
        elif self.model_source == "pinecone":
            if not self.pc:
                raise ValueError("Pinecone client not initialized. Check your API key.")
            
            # Process in batches to avoid exceeding the model's input limit
            batch_size = 32  # Pinecone hosted llama-text-embed-v2 model has a limit of 96 inputs
            all_embeddings = []
            
            for i in tqdm(range(0, len(texts), batch_size), desc="Batches"):
                batch_texts = texts[i:i+batch_size]
                try:
                    # Use Pinecone's hosted llama-text-embed-v2 model
                    response = self.pc.inference.embed(
                        model=self.model_name,
                        inputs=batch_texts,
                        parameters={"input_type": "passage"}
                    )
                    
                    # Extract embedding values
                    batch_embeddings = [item['values'] for item in response]
                    all_embeddings.extend(batch_embeddings)
                except Exception as e:
                    logger.error(f"Error generating embeddings with Pinecone (batch {i//batch_size}): {str(e)}")
                    raise
            
            return np.array(all_embeddings)
