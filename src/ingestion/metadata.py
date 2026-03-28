from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime



# A Template that should be followed by all chunks. Every piece of data is tagged by this template 

class ChunkMetadata(BaseModel):
    # RBAC & Security (Mandatory)
    department: str = Field(..., description="Department this document belongs to (e.g., finance, hr, operations, global)")
    seniority_level: int = Field(default=0, ge=0, le=3, description="Minimum seniority level required (0=employee, 1=analyst, 2=manager, 3=c-suite)")
    
    # Document Identity
    document_id: str = Field(..., description="Unique ID for the source document")
    chunk_index: int = Field(..., description="Sequence number of the chunk in the document")
    
    # Source Tracking
    file_name: str
    file_path: Optional[str] = None
    file_type: str = "pdf"
    
    # Retrieval Enrichment
    page_number: Optional[int] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    # Optional tags for better search
    tags: List[str] = []

    class Config:
        json_schema_extra = {
            "example": {
                "department": "finance",
                "seniority_level": 2,
                "document_id": "doc_123",
                "chunk_index": 5,
                "file_name": "quarterly_results_q4.pdf",
                "page_number": 12,
                "tags": ["revenue", "2023"]
            }
        }
