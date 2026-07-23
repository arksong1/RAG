import json
import logging
from pathlib import Path

from datetime import datetime

from core.load_settings import load_settings


settings = load_settings()
logger = logging.getLogger("ingestion")

def chunk_QuyDinhHB():
    
    file_path = Path(settings["data"]["processed_dir"]) / "quy_dinh_hoc_bong_kkht.json"

    # Kiểm tra file tồn tại
    if not file_path.exists():
        logger.error(f"File not found: {file_path}")
        return []

    # Đọc dữ liệu từ file json
    try: 
        with open(file_path, "r", encoding="utf-8") as f:
            QuyDinhHB = json.load(f)
    # Nếu file không hợp lệ thì báo lỗi
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON from {file_path}: {e}")
        return []

    # Nếu là dict thì chuyển thành list
    if isinstance(QuyDinhHB, dict): 
        QuyDinhHB = [QuyDinhHB]

    # Kiểm tra xem là list không  
    if not isinstance(QuyDinhHB, list):
        logger.error(f"Invalid QuyDinhHB data structure in {file_path}")
        return []

    # Kiểm tra xem có dữ liệu không
    if not QuyDinhHB:
        logger.warning("No QuyDinhHB found in the data")
        return []

    chunks = []

    for idx, QuyDinhHB in enumerate(QuyDinhHB):
        if not isinstance(QuyDinhHB, dict):
            logger.warning(f"Invalid QuyDinhHB at {idx}: expected a dictionary")
            continue

        hb_id = QuyDinhHB.get("id")
        hb_doctitle = QuyDinhHB.get("doc_title")
        if not hb_doctitle or not isinstance(hb_doctitle,str):
            logger.warning(f"Quy dinh hoc bong at index {idx} has invalid or missing title")
            continue

        hb_section = QuyDinhHB.get("section")
        if not hb_section or not isinstance(hb_section,str):
            logger.warning(f"Quy dinh hoc bong at index {idx} has invalid or missing section")
            continue

        hb_content = QuyDinhHB.get("content")
        if not hb_content or not isinstance(hb_content,str):
            logger.warning(f"Quy dinh hoc bong at index {idx} has invalid or missing content")
            continue
        
        base_metadata = {
                "type": "QuyDinhHB",
                "hb_id": hb_id,
                "hb_doctitle": hb_doctitle,
                "hb_section": hb_section,
                "hb_content": hb_content,
                "source": "quy_dinh_hoc_bong_kkht.json",
                "created_at": datetime.utcnow().isoformat(),
                "language": "vi",
            }

        text_parts = (
            f"Quy định học bổng: {hb_doctitle}",
            f"Phần quy định học bổng: {hb_section}",
            f"Nội dung quy định học bổng: {hb_content}",
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
    