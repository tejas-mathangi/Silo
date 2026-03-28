from sentence_transformers import SentenceTransformer
from src.core.config import settings
from typing import List
import numpy as np
import logging

logger = logging.getLogger(__name__)

class DocumentEmbedder:
    def __init__(self):
        logger.info(f"Loading embedding model: {settings.EMBEDDING_MODEL}")
        self.model = SentenceTransformer(settings.EMBEDDING_MODEL, trust_remote_code=True)

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """
        Generates embeddings for a list of strings.
        """
        logger.info(f"Generating embeddings for {len(texts)} chunks")
        embeddings = self.model.encode(texts)
        
        # Convert numpy array to list of lists
        return embeddings.tolist()

# Singleton instance
doc_embedder = DocumentEmbedder()
