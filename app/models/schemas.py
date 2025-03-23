from pydantic import BaseModel, Field
from typing import List, Optional

class QueryRequest(BaseModel):
    """Request model for counseling query"""
    query: str = Field(..., description="The user's query about a mental health challenge")

class SimilarExample(BaseModel):
    """Model for similar counseling examples"""
    context: str
    response: str
    similarity_score: float

class QueryResponse(BaseModel):
    """Response model for counseling query"""
    response: str
    similar_examples: Optional[List[SimilarExample]] = None
    
class StatusResponse(BaseModel):
    """Response model for status endpoint"""
    status: str
