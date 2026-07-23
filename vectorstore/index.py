import logging
import uuid

from embedding.embedder import embed_texts
from core.load_settings import load_settings

settings = load_settings()

logger = logging.getLogger("vector_database") 

# List[Dict] truyền vô là list các chunk và list[dict] trả về là list các point
def build_qdrant_points(chunks: list[dict]) -> list[dict]:
    if not chunks:
        logger.warning("No chunks provided to build Qdrant points")
        return []

    texts = [chunk["text"] for chunk in chunks]
    if not texts:
        logger.warning("No text found in chunks")
        return []

    embeddings = embed_texts(texts)
    if not embeddings:
        logger.warning("Failed to embed texts")
        return []

    points = []

    for chunk, vector in zip(chunks, embeddings): # zip để lấy từng chunk và vector tương ứng 
       points.append({
         "id": str(uuid.uuid4()), # Tạo  id duy nhất cho từng point
         "vector": {"dense": vector}, # embedding vector
         "payload": {
            "text": chunk["text"],
            **chunk.get("metadata", {}) # Thêm metadata nếu có
         }
       })

    logger.info(f"Build {len(points)} Qdrant points")
    return points