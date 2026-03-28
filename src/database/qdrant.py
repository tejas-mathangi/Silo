from qdrant_client import QdrantClient
from qdrant_client.http import models
from src.core.config import settings
import logging

logger = logging.getLogger(__name__)

class QdrantManager:
    def __init__(self):
        self.client = QdrantClient(
            url=settings.QDRANT_URL,
            api_key=settings.QDRANT_API_KEY
        )
        self.collection_name = settings.QDRANT_COLLECTION_NAME

    def init_collection(self):
        """
        Initializes the Qdrant collection with vector configuration and payload indexes.
        """
        # Check if collection exists
        collections = self.client.get_collections().collections
        exists = any(c.name == self.collection_name for c in collections)

        if not exists:
            logger.info(f"Creating collection: {self.collection_name}")
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=settings.EMBEDDING_DIMENSION,
                    distance=models.Distance.COSINE
                )
            )
            
            # Create payload indexes for RBAC filtering performance
            self._create_payload_indexes()
        else:
            logger.info(f"Collection {self.collection_name} already exists.")

    def _create_payload_indexes(self):
        """
        Creates indexes for fields used in RBAC filtering (department and seniority_level).
        """
        logger.info("Creating payload indexes for RBAC...")
        
        # Keyword index for department (exact match)
        self.client.create_payload_index(
            collection_name=self.collection_name,
            field_name="metadata.department",
            field_schema=models.PayloadSchemaType.KEYWORD
        )
        
        # Integer index for seniority_level (range queries: user_level >= doc_level)
        self.client.create_payload_index(
            collection_name=self.collection_name,
            field_name="metadata.seniority_level",
            field_schema=models.PayloadSchemaType.INTEGER
        )
        
        # Document ID for management
        self.client.create_payload_index(
            collection_name=self.collection_name,
            field_name="metadata.document_id",
            field_schema=models.PayloadSchemaType.KEYWORD
        )

    def upsert_chunks(self, points: list[models.PointStruct]):
        """
        Upserts a list of points (vectors + metadata) into the collection.
        """
        return self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )

# Singleton instance
qdrant_manager = QdrantManager()
