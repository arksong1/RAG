import logging
from sentence_transformers import SentenceTransformer

from core.load_settings import load_settings

logger = logging.getLogger("embedding")

settings = load_settings()
EMBEDDING_CONFIG = settings["embedding"]
EMBEDDING_MODEL = EMBEDDING_CONFIG["model"]

_model = None

def get_model() -> SentenceTransformer:
    global _model # Ghi vao bien toan cục
    if _model is None: # Nếu chưa có model thì load 1 lần
        logger.info(f"Loading embedding model: {EMBEDDING_MODEL}")
        _model = SentenceTransformer(EMBEDDING_MODEL, device = EMBEDDING_CONFIG.get("device", "cpu"))
    
    return _model    

def embed_texts(texts: list[str], is_query: bool = False) -> list[list[float]]:
    if not texts:
        logger.warning("No texts providing for embedding")
        return []

    # E5 models require prefixes
    prefix = "query: " if is_query else "passage: "
    prefixed_texts = [f"{prefix}{t}" for t in texts]

    model = get_model()
    embeddings = model.encode(prefixed_texts, normalize_embeddings=True, convert_to_tensor=False).tolist() # chuyen thanh list de luu vao qdrant BAT BUOC
    logger.info(f"Complete embedding texts {len(texts)}")
    return embeddings
