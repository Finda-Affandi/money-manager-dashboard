import os

import requests
from flask import Blueprint, render_template, request, redirect, session, url_for
from google_auth_oauthlib.flow import Flow
from app.config import load_config

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
app_config = load_config('app')


@auth_bp.route('/login', methods=['GET'])
def login():
    """
    Displaying login page

    Returns:
        str: login page
    """

    return render_template('auth/login.html')


@auth_bp.route('/logout')
def logout():
    """
    Logout and delete session

    Returns:
        Response: url login page
    """

    session.pop('credentials', None)
    return redirect(url_for('auth.login'))


@auth_bp.route('/google-auth')
def google_auth():
    """
    authenticating Google SSO

    Returns:
        Response: url google auth page
    """

    flow = Flow.from_client_secrets_file(
        os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'config\\client_secret.json'),
        scopes=app_config.get('SCOPES'),
        redirect_uri=app_config.get('REDIRECT_URI')
    )
    auth_url, _ = flow.authorization_url(prompt='consent')
    return redirect(auth_url)


@auth_bp.route('/callback')
def callback():
    """
    Callbar url redirect from Google

    Returns:
        Response: url to main page if auth success, error message if auth fail
    """

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

    user_info_response = requests.get(
        'https://www.googleapis.com/oauth2/v2/userinfo',
        headers={'Authorization': f'Bearer {credentials.token}'},
        verify=False
    )

    if user_info_response.status_code == 200:
        user_info = user_info_response.json()
        name = user_info.get('name')
        email = user_info.get('email')
        picture = user_info.get('picture')

        session['user'] = {
            'name': name,
            'email': email,
            'picture': picture
        }
        return redirect(url_for('main.index'))
    else:
        return "Error fetching user information", 400
