from src.database.qdrant import qdrant_manager
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    logger.info("Initializing Qdrant...")
    qdrant_manager.init_collection()
    logger.info("Qdrant initialization complete.")

if __name__ == "__main__":
    main()
