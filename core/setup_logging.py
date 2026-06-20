import logging.config
import yaml

from pathlib import Path

def setup_logging():
    project_root = Path(__file__).resolve().parent.parent
    config_path = project_root / "config" / "logging.yaml"
    with open(config_path, encoding="utf-8") as file:
        config = yaml.safe_load(file)
        
    if "handlers" in config and "file" in config["handlers"]:
        filename = config["handlers"]["file"].get("filename")
        if filename:
            log_filepath = project_root / filename
            log_filepath.parent.mkdir(parents=True, exist_ok=True)
            config["handlers"]["file"]["filename"] = str(log_filepath)
            
    logging.config.dictConfig(config) # doc file yaml va chuyen sang python dict