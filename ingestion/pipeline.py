import logging

from ingestion.chunking.QuyCheDaoTao_2346 import chunk_QuyCheDaoTao_2346
from ingestion.chunking.CdrNN import chunk_CdrNN
from ingestion.chunking.QuyDinhHB import chunk_QuyDinhHB
from ingestion.chunking.QuyDinhHP import chunk_QuyDinhHP
from ingestion.chunking.QuyDinhDRL import chunk_QuyDinhDRL

from core.setup_logging import setup_logging
from core.load_settings import load_settings
from vectorstore.upsert import upsert_chunks

setup_logging()
settings = load_settings()
logger = logging.getLogger("ingestion")

def upload_chunks():
    all_chunks = []
    all_chunks.extend(chunk_QuyCheDaoTao_2346())
    all_chunks.extend(chunk_CdrNN())
    all_chunks.extend(chunk_QuyDinhHB())
    all_chunks.extend(chunk_QuyDinhHP())
    all_chunks.extend(chunk_QuyDinhDRL())
    logger.info(f"Total chunks created: {len(all_chunks)}")
    upsert_chunks(all_chunks)
    logger.info("Upsert completed")

if __name__ == "__main__":
    upload_chunks()