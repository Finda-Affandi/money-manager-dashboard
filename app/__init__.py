import os

import urllib3
from flask import Flask
from oauthlib.oauth2 import WebApplicationClient

from app.config import load_config
from app.controller.auth.auth_controller import auth_bp
from app.controller.main_controller import main_bp

app = Flask(__name__)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app_config, web_config = load_config()
app.config.update(app_config)

client = WebApplicationClient(app.config["GOOGLE_CLIENT_ID"])


@app.context_processor
def inject_config():
    return {
        'app_version': app_config.get('APP_VERSION'),
        'web': web_config
    }


app.register_blueprint(main_bp)
app.register_blueprint(auth_bp)
