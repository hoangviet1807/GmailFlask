# AS simeple as possbile flask google oAuth 2.0
from flask import Flask, redirect, url_for, session, render_template    
from authlib.integrations.flask_client import OAuth
import os
from datetime import timedelta


# App config
app = Flask(__name__, template_folder='template')
# Session config
app.secret_key = 'random screct'
app.config['SESSION_COOKIE_NAME'] = 'google-login-session'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)


# oAuth Setup
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id='586049472043-mq10i9qogu3ld4nqets9sd83jvprm78s.apps.googleusercontent.com',
    client_secret='JBsH57_5C1q5OFjEwlKU4aEE',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    # This is only needed if using openId to fetch user info
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
    client_kwargs={'scope': 'openid email profile'},
)


@app.route('/home')
def home():
    email = dict(session).get('email', None)
    return render_template('home.html', email=email)

@app.route('/')
@app.route('/login')
def login():
    google = oauth.create_client('google')  # create the google oauth client
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)


@app.route('/authorize')
def authorize():
    google = oauth.create_client('google')  # create the google oauth client
    # Access token from google (needed to get user info)
    token = google.authorize_access_token()
    # userinfo contains stuff u specificed in the scrope
    resp = google.get('userinfo')
    user_info = resp.json()
    # uses openid endpoint to fetch user info
    # Here you use the profile/user data that you got and query your database find/register the user
    # and set ur own data in the session not the profile from google
    session['email'] = user_info['email']
    # make the session permanant so it keeps existing after broweser gets closed
    return redirect('/home')

# @app.route('/send_mess')
# def send_mess():
#     email =        

@app.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
