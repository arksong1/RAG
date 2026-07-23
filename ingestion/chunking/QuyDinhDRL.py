import json
import logging
from pathlib import Path

from datetime import datetime

from core.load_settings import load_settings


settings = load_settings()
logger = logging.getLogger("ingestion")

def chunk_QuyDinhDRL():
    
    file_path = Path(settings["data"]["processed_dir"]) / "quy_dinh_danh_gia_ren_luyen.json"

    # Kiểm tra file tồn tại
    if not file_path.exists():
        logger.error(f"File not found: {file_path}")
        return []

    # Đọc dữ liệu từ file json
    try: 
        with open(file_path, "r", encoding="utf-8") as f:
            QuyDinhDRL = json.load(f)
    # Nếu file không hợp lệ thì báo lỗi
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON from {file_path}: {e}")
        return []

    # Nếu là dict thì chuyển thành list
    if isinstance(QuyDinhDRL, dict): 
        QuyDinhDRL = [QuyDinhDRL]

    # Kiểm tra xem là list không  
    if not isinstance(QuyDinhDRL, list):
        logger.error(f"Invalid QuyDinhDRL data structure in {file_path}")
        return []

    # Kiểm tra xem có dữ liệu không
    if not QuyDinhDRL:
        logger.warning("No QuyDinhDRL found in the data")
        return []

    chunks = []

    for idx, QuyDinhDRL in enumerate(QuyDinhDRL):
        if not isinstance(QuyDinhDRL, dict):
            logger.warning(f"Invalid QuyDinhDRL at {idx}: expected a dictionary")
            continue

        drl_id = QuyDinhDRL.get("id")
        drl_doctitle = QuyDinhDRL.get("doc_title")
        if not drl_doctitle or not isinstance(drl_doctitle,str):
            logger.warning(f"Quy dinh danh gia ren luyen at index {idx} has invalid or missing title")
            continue
    
        drl_content = QuyDinhDRL.get("content")
        if not drl_content or not isinstance(drl_content,str):
            logger.warning(f"Quy dinh danh gia ren luyen at index {idx} has invalid or missing content")
            continue
        
        base_metadata = {
                "type": "QuyDinhDRL",
                "drl_id": drl_id,
                "drl_doctitle": drl_doctitle,
                "drl_content": drl_content,
                "source": "quy_dinh_danh_gia_ren_luyen.json",
                "created_at": datetime.utcnow().isoformat(),
                "language": "vi",
            }

        text_parts = (
            f"Quy định đánh giá rèn luyện: {drl_doctitle}",
            f"Nội dung quy định đánh giá rèn luyện: {drl_content}",
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
    