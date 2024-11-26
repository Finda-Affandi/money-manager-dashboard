import os

from flask import Blueprint, render_template, request, redirect, session, url_for
from google_auth_oauthlib.flow import Flow
from app.config import load_config

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
app_config = load_config('app')


@auth_bp.route('/login', methods=['GET'])
def login():
    return render_template('auth/login.html')


@auth_bp.route('/google-auth')
def google_auth():
    flow = Flow.from_client_secrets_file(
        os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'config\\client_secret.json'),
        scopes=app_config.get('SCOPES'),
        redirect_uri=app_config.get('REDIRECT_URI')
    )
    auth_url, _ = flow.authorization_url(prompt='consent')
    return redirect(auth_url)


@auth_bp.route('/callback')
def callback():
    flow = Flow.from_client_secrets_file(
        os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'config\\client_secret.json'),
        scopes=app_config.get('SCOPES'),
        redirect_uri=app_config.get('REDIRECT_URI')
    )
    flow.fetch_token(authorization_response=request.url)

    credentials = flow.credentials
    session['credentials'] = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }
    return redirect(url_for('main.index'))
