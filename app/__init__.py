import os
from flask import Flask
from app.config import load_app_config
from app.controller.main_controller import main_bp

app = Flask(__name__)

app_config = load_app_config()
app.config.update(app_config)


@app.context_processor
def inject_config():
    return {
        'app_version': app_config.get('APP_VERSION'),
    }


app.register_blueprint(main_bp)
