import logging

from ingestion.chunking.QuyCheDaoTao_2346 import chunk_QuyCheDaoTao_2346
from core.setup_logging import setup_logging
from core.load_settings import load_settings
from vectorstore.upsert import upsert_chunks

setup_logging()
settings = load_settings()
logger = logging.getLogger("ingestion")

def upload_chunks():
    all_chunks = []
    all_chunks.extend(chunk_QuyCheDaoTao_2346())
    logger.info(f"Total chunks created: {len(all_chunks)}")
    upsert_chunks(all_chunks)
    logger.info("Upsert completed")

if __name__ == "__main__":
    upload_chunks()