import json
import os
from typing import Any, Tuple


def load_all_config(config: str = None) -> tuple[Any, Any] | Any:
    if config == 'app':
        return load_config('app_config.json')
    elif config == 'web':
        return load_config('web_config.json')
    else:
        return load_config('app_config.json'), load_config('web_config.json')


def load_config(file: str):
    config_path = os.path.join(os.path.dirname(__file__), 'config/' + file)
    with open(config_path, 'r') as file:
        config = json.load(file)
    return config
