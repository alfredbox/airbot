import json
from pathlib import Path

RELATIVE_CFG_PATH = ".config/airbot/airbot_cfg.json"

def get_config():
    cfg_path = Path.home().joinpath(RELATIVE_CFG_PATH)
    with cfg_path.open() as f:
        cfg = json.load(f)
        return cfg
