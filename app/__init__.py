import os
from flask import Flask
from app.controller.main_controller import main_bp

app = Flask(__name__)
app.config.from_pyfile(os.path.join(os.path.dirname(__file__), 'config.py'))

app.register_blueprint(main_bp)