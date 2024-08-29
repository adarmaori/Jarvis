import os
import json
from typing import Dict, Any

class ConfigManager:
    _instance = None
    _configs: Dict[str, Any] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
        return cls._instance

    @classmethod
    def load_config(cls, config_name: str) -> Dict[str, Any]:
        if config_name not in cls._configs:
            config_path = os.path.join(os.path.dirname(__file__), f'{config_name}.json')
            try:
                with open(config_path, 'r') as config_file:
                    cls._configs[config_name] = json.load(config_file)
            except FileNotFoundError:
                print(f"Config file '{config_name}.json' not found.")
                cls._configs[config_name] = {}
            except json.JSONDecodeError:
                print(f"Error parsing '{config_name}.json'. Please check the file format.")
                cls._configs[config_name] = {}
        return cls._configs[config_name]

    @classmethod
    def get(cls, config_name: str, key: str, default: Any = None) -> Any:
        config = cls.load_config(config_name)
        return config.get(key, default)
