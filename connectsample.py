import uuid
import requests
from flask import Flask, redirect, url_for, session, request, render_template
from flask_oauthlib.client import OAuth

client_id, client_secret = open('_Private.txt').read().split('\n')

app = Flask(__name__)
app.debug = True
app.secret_key = 'development'
oauth = OAuth(app)


kclForum = oauth.remote_app( \
    'Forum',
    consumer_key=client_id,
    consumer_secret=client_secret,
    request_token_params={'scope': 'User.Read'},
    base_url='https://graph.microsoft.com/v1.0/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://login.microsoftonline.com/common/oauth2/v2.0/token',
    authorize_url='https://login.microsoftonline.com/common/oauth2/v2.0/authorize'
                             )

@app.route('/')
def index():
    """Handler for home page."""
    return render_template('account/connect.html')

@app.route('/login')
def login():
    """Handler for login route."""
    guid = uuid.uuid4() # guid used to only accept initiated logins
    session['state'] = guid
    return kclForum.authorize(callback=url_for('authorized', _external=True), state=guid)

@app.route('/logout')
def logout():
    """Handler for logout route."""
    session.pop('microsoft_token', None)
    session.pop('state', None)
    return redirect(url_for('index'))

@app.route('/login/authorized')
def authorized():
    """Handler for login/authorized route."""
    response = kclForum.authorized_response()

    if response is None:
        return "Access Denied: Reason={0}\nError={1}".format( \
            request.args['error'], request.args['error_description'])

    # Check response for state
    if str(session['state']) != str(request.args['state']):
        raise Exception('State has been messed with, end authentication')
    session['state'] = '' # reset session state to prevent re-use

    # Okay to store this in a local variable, encrypt if it's going to client
    # machine or database. Treat as a password.
    session['microsoft_token'] = (response['access_token'], '')
    # Store the token in another session variable for easy access
    session['access_token'] = response['access_token']
    me_response = kclForum.get('me')
    me_data = json.loads(json.dumps(me_response.data))
    username = me_data['displayName']
    email_address = me_data['userPrincipalName']
    if not email_address.endswith('kcl.ac.uk'):
        return render_template('badRequest.html')
    session['alias'] = username
    session['userEmailAddress'] = email_address
    return redirect('main')

@app.route('/main')
def main():
    """Handler for main route."""
    if session['alias']:
        username = session['alias']
        email_address = session['userEmailAddress']

        return render_template('main.html', name=username, emailAddress=email_address)
    else:
        return render_template('main.html')


@kclForum.tokengetter
def get_token():
    """Return the Oauth token."""
    return session.get('microsoft_token')

