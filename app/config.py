import json
import os


def load_app_config():
    app_config_path = os.path.join(os.path.dirname(__file__), 'config/app_config.json')
    with open(app_config_path, 'r') as file:
        app_config = json.load(file)

    return app_config
