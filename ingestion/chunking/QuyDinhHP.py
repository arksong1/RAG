import json
import logging
from pathlib import Path

from datetime import datetime

from core.load_settings import load_settings


settings = load_settings()
logger = logging.getLogger("ingestion")

def chunk_QuyDinhHP():
    
    file_path = Path(settings["data"]["processed_dir"]) / "quy_dinh_thu_nop_hoc_phi.json"

    # Kiểm tra file tồn tại
    if not file_path.exists():
        logger.error(f"File not found: {file_path}")
        return []

    # Đọc dữ liệu từ file json
    try: 
        with open(file_path, "r", encoding="utf-8") as f:
            QuyDinhHP = json.load(f)
    # Nếu file không hợp lệ thì báo lỗi
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON from {file_path}: {e}")
        return []

    # Nếu là dict thì chuyển thành list
    if isinstance(QuyDinhHP, dict): 
        QuyDinhHP = [QuyDinhHP]

    # Kiểm tra xem là list không  
    if not isinstance(QuyDinhHP, list):
        logger.error(f"Invalid QuyDinhHP data structure in {file_path}")
        return []

    # Kiểm tra xem có dữ liệu không
    if not QuyDinhHP:
        logger.warning("No QuyDinhHP found in the data")
        return []

    chunks = []

    for idx, QuyDinhHP in enumerate(QuyDinhHP):
        if not isinstance(QuyDinhHP, dict):
            logger.warning(f"Invalid QuyDinhHB at {idx}: expected a dictionary")
            continue

        hp_id = QuyDinhHP.get("id")
        hp_doctitle = QuyDinhHP.get("doc_title")
        if not hp_doctitle or not isinstance(hp_doctitle,str):
            logger.warning(f"Quy dinh hoc bong at index {idx} has invalid or missing title")
            continue

        hp_section = QuyDinhHP.get("section")
        if not hp_section or not isinstance(hp_section,str):
            logger.warning(f"Quy dinh hoc bong at index {idx} has invalid or missing section")
            continue
        
        hp_content = QuyDinhHP.get("content")
        if not hp_content or not isinstance(hp_content,str):
            logger.warning(f"Quy dinh hoc bong at index {idx} has invalid or missing content")
            continue
        
        base_metadata = {
                "type": "QuyDinhHP",
                "hp_id": hp_id,
                "hp_doctitle": hp_doctitle,
                "hp_content": hp_content,
                "source": "quy_dinh_thu_nop_hoc_phi.json",
                "created_at": datetime.utcnow().isoformat(),
                "language": "vi",
            }

        text_parts = (
            f"Quy định học phí: {hp_doctitle}",
            f"Phần quy định học phí: {hp_section}",
            f"Nội dung quy định học phí: {hp_content}",
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
    