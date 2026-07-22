import sys
import json
import logging
from pathlib import Path

# Add project root to sys.path to enable imports of core
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

from core.load_settings import load_settings
from core.setup_logging import setup_logging

setup_logging()
settings = load_settings()
logger = logging.getLogger("ingestion")

def load_data():
    raw_dir = project_root / settings["data"]["raw_dir"]
    processed_dir = project_root / settings["data"]["processed_dir"]
    
    data = json.load(open(raw_dir / "quy_che_dao_tao_2346_MDC.json", "r", encoding="utf-8"))
    
    if not data:
        logger.error("No raw data found")
        return 

    if isinstance(data, list):
        processed_dir.mkdir(parents=True, exist_ok=True)
        output_path = processed_dir / "quy_che_dao_tao_2346_MDC.json"
        with open(output_path, "w", encoding="utf-8") as outfile:
            json.dump(data, outfile, ensure_ascii=False, indent=3)
        logger.info(f"Data written to {output_path}")
        return

    tables = data.get("tables", {})

    if not tables:
        logger.warning("No tables found")
        return 

    # Ensure processed directory exists
    processed_dir.mkdir(parents=True, exist_ok=True)

    # table_name: ten bang, table_data: du lieu trong bang
    for table_name, table_data in tables.items(): 
        if not table_data:
            logger.warning(f"No data for table {table_name}")
            continue
        
        # tao duong dan file json moi cho tung bang
        output_path = processed_dir / f"{table_name}.json" 
        
        # mo file de ghi du lieu
        with open(output_path, "w", encoding="utf-8") as outfile: 
            # ensure_ascii=False de giu nguyen tieng viet, indent=4 de format lai file de doc hon
            json.dump(table_data, outfile, ensure_ascii=False, indent=3) 
            
        logger.info(f"Data for table {table_name} written to {output_path}")

        
if __name__ == "__main__":
    load_data()       