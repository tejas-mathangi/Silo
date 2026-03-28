from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List, Dict, Any
from src.ingestion.metadata import ChunkMetadata
import uuid
import logging

logger = logging.getLogger(__name__)

class DocumentChunker:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.splitter = RecursiveCharacterTextSplitter(  # Doesn't split randomly, splits at good places such as paragraph break (\n\n), or single line etc.,
            chunk_size=chunk_size,  # 1000 char
            chunk_overlap=chunk_overlap,  # Each chunk includes some part before and some part after it of 200 char
            length_function=len,
            is_separator_regex=False,
        )

    def chunk_document(
        self, 
        content: str, 
        department: str, 
        seniority_level: int, 
        file_info: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Splits content into chunks and attaches RBAC-compliant metadata.
        """
        logger.info(f"Chunking document: {file_info['file_name']}")
        
        # Split text
        texts = self.splitter.split_text(content)
        
        # Create a unique ID for the document
        document_id = str(uuid.uuid4())
        
        chunks = []
        for i, text in enumerate(texts):
            # Create RBAC-compliant metadata
            metadata = ChunkMetadata(
                department=department,
                seniority_level=seniority_level,
                document_id=document_id,
                chunk_index=i,
                file_name=file_info["file_name"],
                file_path=file_info["file_path"],
                file_type=file_info["file_type"]
            )
            
            chunks.append({
                "content": text,
                "metadata": metadata.model_dump()
            })
            
        return chunks

# Singleton instance
doc_chunker = DocumentChunker()
