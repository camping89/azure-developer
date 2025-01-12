from flask import render_template, redirect, request, session, url_for
from flask_login import current_user, login_user, logout_user, login_required
import msal
import uuid
from config import Config
from FlaskExercise import app
from FlaskExercise.models import User

import requests

@app.route('/')
@app.route('/home')
@login_required
def home():
    return render_template('index.html', email=session['user']['preferred_username'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    session['state'] = str(uuid.uuid4())
    # Note: Below will return None as an auth_url until you implement the function
    auth_url = _build_auth_url(scopes=Config.SCOPE, state=session['state'])
    return render_template('login.html',
                           title=f'Sign In at {get_public_ip()}',
                           auth_url=auth_url)


@app.route('/logout')
def logout():
    logout_user()  # Log out of Flask session
    if session.get('user'):  # Used MS Login
        # Wipe out user and its token cache from session
        session.clear()
        return redirect(
            Config.AUTHORITY + '/oauth2/v2.0/logout' +
            '?post_logout_redirect_uri=' + url_for('login', _external=True))
        pass

    return redirect(url_for('login'))


@app.route(Config.REDIRECT_PATH)  # Its absolute URL must match your app's redirect_uri set in AAD
def authorized():
    if request.args.get('state') != session.get('state'):
        return redirect(url_for('home'))  # Failed, go back home
    if 'error' in request.args:  # Authentication/Authorization failure
        return render_template('auth_error.html', result=request.args)
    if request.args.get('code'):
        cache = _load_cache()
        result = _build_msal_app(cache=cache).acquire_token_by_authorization_code(
            request.args['code'],
            scopes=Config.SCOPE,
            redirect_uri=url_for('authorized', _external=True, _scheme='https')
        )
        if 'error' in result:
            return render_template('auth_error.html', result=result)
        session['user'] = result.get('id_token_claims')
        # Note: In a real app, use the appropriate user's DB ID below,
        #   but here, we'll just log in with a fake user zero
        #   This is so flask login functionality works appropriately.
        user = User(0)
        login_user(user)
        _save_cache(cache)

    return redirect(url_for('home'))


def _load_cache():
    cache = msal.SerializableTokenCache()
    if session.get('token_cache'):
        cache.deserialize(session['token_cache'])
    return cache


def _save_cache(cache):
    if cache.has_state_changed:
        session['token_cache'] = cache.serialize()


def _build_msal_app(cache=None, authority=None):
    return msal.ConfidentialClientApplication(Config.APPLICATION_CLIENT_ID,
                                              authority=authority or Config.AUTHORITY,
                                              client_credential=Config.CLIENT_SECRET,
                                              token_cache=cache)


def _build_auth_url(authority=None, scopes=None, state=None):
    return _build_msal_app(authority=authority).get_authorization_request_url(
        scopes or [],
        state=state or str(uuid.uuid4()),
        redirect_uri=url_for('authorized', _external=True, _scheme='https'))

def get_public_ip():
    try:
        # Make a request to an external service to get the public IP address
        response = requests.get('https://api.ipify.org?format=json')
        response.raise_for_status()  # Raise an exception for any HTTP errors
        ip_data = response.json()
        return ip_data["ip"]
    except requests.RequestException as e:
        return f"Error fetching IP: {e}"