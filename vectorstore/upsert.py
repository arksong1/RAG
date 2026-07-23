import logging
from qdrant_client import QdrantClient

from core.load_settings import load_settings
from vectorstore.qdrant import get_qdrant_client, ensure_collection
from vectorstore.index import build_qdrant_points

settings = load_settings()
logger = logging.getLogger("vector_database")

QDRANT_CONFIG = settings["vector_database"]
COLLECTION_NAME = QDRANT_CONFIG["collection_name"]
# ham nay nhan vao list cac chunk va them vao qdrant
def upsert_chunks(chunks: list[dict]):
    if not chunks:
        logger.warning("No chunks provided")
        return []

    client: QdrantClient = get_qdrant_client() # Lấy client từ qdrant.py
    ensure_collection(client) # Đảm bảo client tồn tại
    points = build_qdrant_points(chunks) # Tạo point từ các chunks

    if not points:
        logger.warning("No points were built from provided chunk.")
        return []

    client.upsert(collection_name=COLLECTION_NAME, points=points) # upsert points vao collection
    logger.info(f"Upserted {len(points)} points into collection '{COLLECTION_NAME}'")