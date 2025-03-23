from fastapi import APIRouter, Depends, HTTPException, status
from app.models.schemas import QueryRequest, QueryResponse, StatusResponse, SimilarExample
from app.services.vector_db import VectorDBService
from app.services.embedding import EmbeddingService
from app.services.llm import LLMService
from app.config import DATASET_PATH
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

# Global service instances
_vector_db = None
_llm_service = None

# Dependency to get services
def get_vector_db():
    global _vector_db
    if _vector_db is None:
        embedding_service = EmbeddingService()
        _vector_db = VectorDBService(embedding_service)
        # Try to initialize the vector database
        try:
            # _vector_db.load_data(DATASET_PATH)
            logger.info("Vector database initialized on first request")
        except Exception as e:
            logger.error(f"Failed to initialize vector database: {str(e)}")
            # Continue without initialization, will try again on the query endpoint
    return _vector_db

def get_llm_service():
    global _llm_service
    if _llm_service is None:
        _llm_service = LLMService()
    return _llm_service

@router.post("/query", response_model=QueryResponse)
async def query_endpoint(
    request: QueryRequest,
    vector_db: VectorDBService = Depends(get_vector_db),
    llm_service: LLMService = Depends(get_llm_service)
):
    """
    Process a mental health query and return a counseling response
    """
    logger.info(f"Received query: {request.query[:50]}...")
    
    # Check if index exists and create if not
    if vector_db.index is None:
        try:
            vector_db.load_data(DATASET_PATH)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to load dataset: {str(e)}"
            )
    
    # Find similar examples
    similar_results = vector_db.search(request.query)
    
    # Generate response using LLM
    response_text = llm_service.generate_response(request.query, similar_results)
    
    # Format similar examples for response
    similar_examples = [
        SimilarExample(
            context=item["Context"],
            response=item["Response"],
            similarity_score=item["similarity_score"]
        ) for item in similar_results
    ]
    
    return QueryResponse(
        response=response_text,
        similar_examples=similar_examples
    )

@router.get("/status", response_model=StatusResponse)
async def status_endpoint():
    """
    Health check endpoint
    """
    return StatusResponse(status="ok")
