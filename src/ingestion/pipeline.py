from typing import List, Dict, Any
from src.ingestion.parser import doc_parser
from src.ingestion.chunker import doc_chunker
from src.ingestion.embedder import doc_embedder
from src.database.qdrant import qdrant_manager
from qdrant_client.http import models
import uuid
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class IngestionPipeline:
    def __init__(self):
        self.parser = doc_parser
        self.chunker = doc_chunker
        self.embedder = doc_embedder
        self.db = qdrant_manager

    def run(self, file_path: str, department: str, seniority_level: int):
        """
        Runs the full ingestion pipeline for a single document.
        """
        logger.info(f"Starting ingestion for: {file_path}")

        # 1. Parse
        parsed_doc = self.parser.parse(file_path)
        
        # 2. Chunk
        chunks = self.chunker.chunk_document(
            content=parsed_doc["content"],
            department=department,
            seniority_level=seniority_level,
            file_info=parsed_doc["file_info"]
        )

        # 3. Embed
        texts = [c["content"] for c in chunks]
        embeddings = self.embedder.embed_texts(texts)

        # 4. Store in Qdrant
        points = []
        for i, (chunk, vector) in enumerate(zip(chunks, embeddings)):
            point_id = str(uuid.uuid4())
            points.append(models.PointStruct(
                id=point_id,
                vector=vector,
                payload={
                    "content": chunk["content"],
                    "metadata": chunk["metadata"]
                }
            ))

        logger.info(f"Upserting {len(points)} points to Qdrant...")
        self.db.upsert_chunks(points)
        logger.info(f"Successfully ingested: {file_path}")

# Singleton instance
ingestion_pipeline = IngestionPipeline()
