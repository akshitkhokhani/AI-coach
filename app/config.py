import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

try:
    # API settings
    API_PREFIX = "/api/v1"

    # OpenAI settings
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")

    # Vector database settings
    VECTOR_DB_TYPE = os.getenv("VECTOR_DB_TYPE", "pinecone")
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    PINECONE_CLOUD = os.getenv("PINECONE_CLOUD", "aws")  # 'aws' or 'gcp'
    PINECONE_REGION = os.getenv("PINECONE_REGION", "us-east-1")  # e.g., 'us-east-1', 'us-west-2', etc.
    PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "llama-text-embed-v2-index")
    PINECONE_NAMESPACE = os.getenv("PINECONE_NAMESPACE", "counseling")
    PINECONE_DIMENSION = 1024  # llama-text-embed-v2 dimension size
    PINECONE_METRIC = "cosine"

    # Embedding model settings
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "llama-text-embed-v2")
    EMBEDDING_MODEL_SOURCE = os.getenv("EMBEDDING_MODEL_SOURCE", "pinecone")

    # Data settings
    DATASET_PATH = os.getenv("DATASET_PATH", "data/train.csv")

    # Similarity search settings
    TOP_K_RESULTS = int(os.getenv("TOP_K_RESULTS", "5"))

except:
    import os
    import streamlit as st
    from dotenv import load_dotenv

    # Load environment variables from .env file for local development
    load_dotenv()

    # API settings
    API_PREFIX = "/api/v1"

    # Load keys from secrets or environment variables
    # OpenAI settings
    OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY"))
    OPENAI_MODEL = st.secrets.get("OPENAI_MODEL", os.getenv("OPENAI_MODEL", "gpt-4"))

    # Vector database settings
    VECTOR_DB_TYPE = st.secrets.get("VECTOR_DB_TYPE", os.getenv("VECTOR_DB_TYPE", "pinecone"))
    PINECONE_API_KEY = st.secrets.get("PINECONE_API_KEY", os.getenv("PINECONE_API_KEY"))
    PINECONE_CLOUD = st.secrets.get("PINECONE_CLOUD", os.getenv("PINECONE_CLOUD", "aws"))
    PINECONE_REGION = st.secrets.get("PINECONE_REGION", os.getenv("PINECONE_REGION", "us-east-1"))
    PINECONE_INDEX_NAME = st.secrets.get("PINECONE_INDEX_NAME", os.getenv("PINECONE_INDEX_NAME", "llama-text-embed-v2-index"))
    PINECONE_NAMESPACE = st.secrets.get("PINECONE_NAMESPACE", os.getenv("PINECONE_NAMESPACE", "counseling"))
    PINECONE_DIMENSION = 1024  # llama-text-embed-v2 dimension size
    PINECONE_METRIC = "cosine"

    # Embedding model settings
    EMBEDDING_MODEL = st.secrets.get("EMBEDDING_MODEL", os.getenv("EMBEDDING_MODEL", "llama-text-embed-v2"))
    EMBEDDING_MODEL_SOURCE = st.secrets.get("EMBEDDING_MODEL_SOURCE", os.getenv("EMBEDDING_MODEL_SOURCE", "pinecone"))

    # Data settings
    DATASET_PATH = os.getenv("DATASET_PATH", "data/train.csv")

    # Similarity search settings
    TOP_K_RESULTS = int(st.secrets.get("TOP_K_RESULTS", os.getenv("TOP_K_RESULTS", "5")))