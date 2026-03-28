from src.ingestion.pipeline import ingestion_pipeline
from src.database.qdrant import qdrant_manager
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def seed_data():
    # 1. Initialize Qdrant Collection
    logger.info("Initializing Qdrant collection...")
    qdrant_manager.init_collection()

    # 2. Define sample documents to ingest
    samples = [
        {
            "path": "src/data/finance_policy.md",
            "department": "finance",
            "seniority_level": 2  # Manager Level
        }
    ]

    # 3. Run ingestion for each sample
    for sample in samples:
        file_path = sample["path"]
        if not Path(file_path).exists():
            logger.error(f"Sample file not found: {file_path}")
            continue
            
        logger.info(f"Ingesting {file_path} for {sample['department']} (Level {sample['seniority_level']})")
        ingestion_pipeline.run(
            file_path=file_path,
            department=sample["department"],
            seniority_level=sample["seniority_level"]
        )

if __name__ == "__main__":
    seed_data()
