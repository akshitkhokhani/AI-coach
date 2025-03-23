import os
import logging
import pandas as pd
from dotenv import load_dotenv
from app.services.vector_db import VectorDBService
from app.services.embedding import EmbeddingService
from app.config import PINECONE_API_KEY, PINECONE_INDEX_NAME

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)

def main():
    # Load environment variables
    load_dotenv()
    
    # Validate API key
    if not PINECONE_API_KEY:
        logger.error("Missing PINECONE_API_KEY in environment variables")
        return
        
    # Path to your training data CSV
    data_path = "train.csv"  # Update this to your actual path
    
    if not os.path.exists(data_path):
        logger.error(f"Data file not found: {data_path}")
        return
    
    # Initialize services
    try:
        logger.info("Initializing embedding service with Pinecone")
        embedding_service = EmbeddingService(model_source="pinecone", model_name="llama-text-embed-v2")
        vector_db = VectorDBService(embedding_service)
        
        # Load dataset
        logger.info(f"Loading dataset from {data_path}")
        df = pd.read_csv(data_path)
        
        if 'Context' not in df.columns or 'Response' not in df.columns:
            logger.error("Dataset must contain 'Context' and 'Response' columns")
            return
            
        # Process data in smaller batches to avoid potential issues
        batch_size = 30
        total_records = 0
        
        for i in range(0, len(df), batch_size):
            batch_df = df.iloc[i:i+batch_size]
            logger.info(f"Processing batch {i//batch_size + 1}/{(len(df)-1)//batch_size + 1} ({len(batch_df)} records)")
            
            # Load batch into vector database
            try:
                vector_db.load_data(batch_df)
                total_records += len(batch_df)
                logger.info(f"Successfully loaded batch into vector database")
            except Exception as e:
                logger.error(f"Failed to load batch: {str(e)}")
                
        logger.info(f"Successfully loaded total of {total_records} records into vector database")
    except Exception as e:
        logger.error(f"Failed to load data: {str(e)}")

if __name__ == "__main__":
    main()
