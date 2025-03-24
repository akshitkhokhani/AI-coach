import streamlit as st
import logging
from app.services.vector_db import VectorDBService
from app.services.embedding import EmbeddingService
from app.services.llm import LLMService
from app.models.schemas import SimilarExample
from app.config import DATASET_PATH

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize services (once when the app loads)
@st.cache_resource
def initialize_services():
    embedding_service = EmbeddingService()
    vector_db = VectorDBService(embedding_service)
    
    # Try to initialize the vector database
    try:
        vector_db.load_data(DATASET_PATH)
        logger.info("Vector database initialized")
    except Exception as e:
        logger.error(f"Failed to initialize vector database: {str(e)}")
    
    llm_service = LLMService()
    return vector_db, llm_service

# Get services
vector_db, llm_service = initialize_services()

# App title and description
st.title("Mental Health Counseling Assistant")
st.write("Ask a question and get a counseling response based on similar examples.")

# Input field for user query
user_query = st.text_area("Enter your question or concern:", height=100)

# Process query when button is clicked
if st.button("Get Response") and user_query:
    with st.spinner("Processing your question..."):
        try:
            # Check if index exists and create if not
            if vector_db.index is None:
                try:
                    vector_db.load_data(DATASET_PATH)
                except Exception as e:
                    st.error(f"Failed to load dataset: {str(e)}")
                    st.stop()
            
            # Find similar examples
            logger.info(f"Processing query: {user_query[:50]}...")
            similar_results = vector_db.search(user_query)
            
            # Generate response using LLM
            response_text = llm_service.generate_response(user_query, similar_results)
            print(response_text)
            
            # Format similar examples
            similar_examples = [
                SimilarExample(
                    context=item["Context"],
                    response=item["Response"],
                    similarity_score=item["similarity_score"]
                ) for item in similar_results
            ]
            
            # Display response
            st.subheader("Response:")
            st.write(response_text)
            
            # Display similar examples in an expandable section
            with st.expander("View similar examples used to generate this response"):
                for i, example in enumerate(similar_examples):
                    st.markdown(f"**Example {i+1}** (Similarity score: {example.similarity_score:.2f})")
                    st.markdown("**Context:**")
                    st.write(example.context)
                    st.markdown("**Response:**") 
                    st.write(example.response)
                    st.divider()
                    
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            logger.error(f"Error processing query: {str(e)}")

# Display app status
st.sidebar.subheader("App Status")
if vector_db.index is not None:
    st.sidebar.success("Vector database loaded and ready")
else:
    st.sidebar.warning("Vector database not yet loaded")