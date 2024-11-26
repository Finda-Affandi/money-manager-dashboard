import json
import os
from typing import Any, Tuple


def load_config(config: str = None) -> tuple[Any, Any] | Any:
    if config == 'app':
        return __load('app_config.json')
    elif config == 'web':
        return __load('web_config.json')
    else:
        return __load('app_config.json'), __load('web_config.json')


def __load(file: str):
    config_path = os.path.join(os.path.dirname(__file__), 'config/' + file)
    with open(config_path, 'r') as file:
        config = json.load(file)
    return config
