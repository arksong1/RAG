import json
import logging
from pathlib import Path

from datetime import datetime

from core.settings_loader import load_settings
from ingestion.helpers.make_metadata import make_metadata

settings = load_settings()
logger = logging.getLogger("ingestion")

def chunk_QuyCheDaoTao_2346():
    # Khai bao file path
    file_path = Path(settings["data"]["processed_dir"]) / "quy_che_dao_tao_2346_MDC.json"

    # Kiểm tra file tồn tại
    if not file_path.exists():
        logger.error(f"File not found: {file_path}")
        return []

    # Đọc dữ liệu từ file json
    try: 
        with open(file_path, "r", encoding="utf-8") as f:
            quy_che_dao_tao_2346_MDC = json.load(f)
    # Nếu file không hợp lệ thì báo lỗi
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON from {file_path}: {e}")
        return []
    
    # Nếu là dict thì chuyển thành list
    if isinstance(quy_che_dao_tao_2346_MDC, dict): 
        quy_che_dao_tao_2346_MDC = [quy_che_dao_tao_2346_MDC]

    # Kiểm tra xem là list không  
    if not isinstance(quy_che_dao_tao_2346_MDC, list):
        logger.error(f"Invalid QuyCheDaoTao_2346_MDC data structure in {file_path}")
        return []
    
    # Kiểm tra xem có dữ liệu không
    if not quy_che_dao_tao_2346_MDC:
        logger.warning("No QuyCheDaoTao_2346_MDC found in the data")
        return []

    chunks = []

    for idx, quy_che_dao_tao_2346_MDC in enumerate(quy_che_dao_tao_2346_MDC):
        if not isinstance(quy_che_dao_tao_2346_MDC, dict):
            logger.warning(f"Invalid QuyCheDaoTao_2346_MDC at index {idx}: expected a dictionary")
            continue

        quyche_id = quy_che_dao_tao_2346_MDC.get("id")
        quyche_title = quy_che_dao_tao_2346_MDC.get("document_title")
        if not quyche_title or not isinstance(quyche_title,str):
            logger.warning(f"Quy che dao tao at index {idx} has invalid or missing title")
            continue
        quyche_chapter_title =  quy_che_dao_tao_2346_MDC.get("chapter_title")
        if quyche_chapter_title and not isinstance(quyche_chapter_title, str):
            logger.warning(f"Quy che dao tao at index {idx} has invalid or missing chapter title")
            continue
        quyche_article_number =  quy_che_dao_tao_2346_MDC.get("article_number")
        if quyche_article_number and not isinstance(quyche_article_number, str):
            logger.warning(f"Quy che dao tao at index {idx} has invalid or missing article number")
            continue
        quyche_article_title =  quy_che_dao_tao_2346_MDC.get("article_title")
        if quyche_article_title and not isinstance(quyche_article_title, str):
            logger.warning(f"Quy che dao tao at index {idx} has invalid or missing article title")
            continue
        
        quyche_path = quy_che_dao_tao_2346_MDC.get("path")
        
        quyche_text = quy_che_dao_tao_2346_MDC.get("text")
        if quyche_text and not isinstance(quyche_text, str):
            logger.warning(f"Quy che dao tao at index {idx} has invalid or missing text")
            continue

        if not quyche_title:
            logger.warning(f"Quy che dao tao at index {idx} has invalid or missing title")
            continue

        base_metadata = {
            "type": "quyche_dao_tao_2346_MDC",
            "quyche_id": quyche_id,
            "quyche_title": quyche_title,
            "quyche_chapter_title": quyche_chapter_title,
            "quyche_article_number": quyche_article_number,
            "quyche_article_title": quyche_article_title,
            "quyche_path": quyche_path,
            "quyche_text": quyche_text,
            "source": "quy_che_dao_tao_2346_MDC.json",
            "created_at": datetime.utcnow().isoformat(),
            "language": "vi",
        }

        text_parts = (
            f"Tên quy chế: {quyche_title}",
            f"Chương: {quyche_chapter_title}",
            f"Điều: {quyche_article_number}",
            f"Tiêu đề điều: {quyche_article_title}",
            f"Nội dung điều: {quyche_text}",
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