import os
from flask import Flask
from app.config import load_all_config
from app.controller.main_controller import main_bp

app = Flask(__name__)

app_config, web_config = load_all_config()
app.config.update(app_config)


@app.context_processor
def inject_config():
    return {
        'app_version': app_config.get('APP_VERSION'),
        'web': web_config
    }


app.register_blueprint(main_bp)
