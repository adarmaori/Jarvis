from typing import Dict, Any
import os
import json

MAIN_CONFIG_PATH = os.path.join(os.path.dirname(__file__), f'../config/main.json')


def get_config(config_name: str) -> Dict[str, Any]:
    config_path = os.path.join(os.path.dirname(__file__), f'../config/{config_name}.json')
    with open(config_path, 'r') as config_file:
        return json.load(config_file)
