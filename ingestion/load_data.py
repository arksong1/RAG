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
    # raw_dir = project_root / settings["data"]["raw_dir"]
    # processed_dir = project_root / settings["data"]["processed_dir"]
    
    data = json.load(open(Path(settings["data"]["raw_dir"]) / "database_export_2026-01-23T02-02-46.json", "r", encoding="utf-8"))
    # # Find the database export file dynamically
    # export_files = list(raw_dir.glob("database_export_*.json"))
    # if not export_files:
    #     logger.error(f"No database export file found in {raw_dir}")
    #     return

    # # Use the latest export file based on lexicographical sorting
    # export_file = sorted(export_files)[-1]
    # logger.info(f"Loading raw data from {export_file}")

    # try:
    #     with open(export_file, "r", encoding="utf-8") as infile:
    #         data = json.load(infile)
    # except Exception as e:
    #     logger.error(f"Failed to load raw data: {e}")
    #     return

    if not data:
        logger.error("No raw data found")
        return 

    tables = data.get("tables", {})

    if not tables:
        logger.warning("No tables found")
        return 

    # Ensure processed directory exists
    # processed_dir.mkdir(parents=True, exist_ok=True)

    # table_name: ten bang, table_data: du lieu trong bang
    for table_name, table_data in tables.items(): 
        if not table_data:
            logger.warning(f"No data for table {table_name}")
            continue
        
        # tao duong dan file json moi cho tung bang
        output_path = Path(settings["data"]["processed_dir"]) / f"{table_name}.json" 
        
        # mo file de ghi du lieu
        with open(output_path, "w", encoding="utf-8") as outfile: 
            # ensure_ascii=False de giu nguyen tieng viet, indent=4 de format lai file de doc hon
            json.dump(table_data, outfile, ensure_ascii=False, indent=4) 
            
        logger.info(f"Data for table {table_name} written to {output_path}")
        

        
if __name__ == "__main__":
    load_data()       