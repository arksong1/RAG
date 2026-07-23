import json
import logging
from pathlib import Path

from datetime import datetime

from core.load_settings import load_settings

settings = load_settings()
logger = logging.getLogger("ingestion")

def chunk_CdrNN():
    
    file_path = Path(settings["data"]["processed_dir"]) / "chuan_ngoai_ngu_cntt_MDC.json"

    # Kiểm tra file tồn tại
    if not file_path.exists():
        logger.error(f"File not found: {file_path}")
        return []

    # Đọc dữ liệu từ file json
    try: 
        with open(file_path, "r", encoding="utf-8") as f:
            CdrNN = json.load(f)
    # Nếu file không hợp lệ thì báo lỗi
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON from {file_path}: {e}")
        return []

    # Nếu là dict thì chuyển thành list
    if isinstance(CdrNN, dict): 
        CdrNN = [CdrNN]

    # Kiểm tra xem là list không  
    if not isinstance(CdrNN, list):
        logger.error(f"Invalid CdrNN data structure in {file_path}")
        return []

    # Kiểm tra xem có dữ liệu không
    if not CdrNN:
        logger.warning("No CdrNN found in the data")
        return []

    chunks = []

    for idx, CdrNN in enumerate(CdrNN):
        if not isinstance(CdrNN, dict):
            logger.warning(f"Invalid CdrNN at {idx}: expected a dictionary")
            continue

        cdr_id = CdrNN.get("id")

        cdr_doctitle = CdrNN.get("document_title")
        if not cdr_doctitle or not isinstance(cdr_doctitle,str):
            logger.warning(f"Quy dinh hoc bong at index {idx} has invalid or missing title")
            continue

        cdr_arttitle = CdrNN.get("article_title", "")
        if not cdr_arttitle or not isinstance(cdr_arttitle,str):
            logger.warning(f"Quy dinh hoc bong at index {idx} has invalid or missing section")
            continue
        
        cdr_text = CdrNN.get("text")
        if not cdr_text or not isinstance(cdr_text,str):
            logger.warning(f"Quy dinh hoc bong at index {idx} has invalid or missing content")
            continue
        
        base_metadata = {
                "type": "CdrNN",
                "cdr_id": cdr_id,
                "cdr_doctitle": cdr_doctitle,
                "cdr_arttitle": cdr_arttitle,
                "cdr_text": cdr_text,
                "source": "chuan_ngoai_ngu_cntt_MDC.json",
                "created_at": datetime.utcnow().isoformat(),
                "language": "vi",
            }

        text_parts = (
            f"Quy định chuẩn đầu ra ngoại ngữ: {cdr_doctitle}",
            f"Phần quy định chuẩn đầu ra ngoại ngữ: {cdr_arttitle}",
            f"Nội dung quy định chuẩn đầu ra ngoại ngữ: {cdr_text}",
        )
        text = "\n".join(text_parts)
        chunks.append(
            {
                "text": text,
                "metadata": base_metadata,
            }
        )
        
    if not chunks:
        logger.warning("No chunks created")
    return chunks
    