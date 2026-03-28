from qdrant_client import QdrantClient
from src.core.config import settings
from src.ingestion.embedder import doc_embedder
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_retrieval(query: str):
    # 1. Initialize Client (talking to the Docker container)
    client = QdrantClient(url=settings.QDRANT_URL)
    
    # 2. Generate embedding for the query
    logger.info(f"Querying: '{query}'")
    query_vector = doc_embedder.embed_texts([query])[0]
    
    # 3. Search in Qdrant
    results = client.query_points(
        collection_name=settings.QDRANT_COLLECTION_NAME,
        query=query_vector,
        limit=3
    ).points
    
    # 4. Print results
    print("\n--- Retrieval Results ---")
    for i, res in enumerate(results):
        print(f"\nResult {i+1} (Score: {res.score:.4f}):")
        print(f"Content: {res.payload['content'][:200]}...")
        print(f"Metadata: {res.payload['metadata']}")

if __name__ == "__main__":
    # Test with a question about the finance policy we ingested
    test_retrieval("What is the policy for expense reimbursements?")
