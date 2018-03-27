import requests
from config import BaseConfig
from flask import Flask, render_template, request, redirect, Markup, session
from oauth_fiware import OAuth2

try:
    import simplejson as json
except ImportError:
    import json

app = Flask(__name__)
app.config.from_object(BaseConfig)

auth_app = OAuth2()


@app.route('/reset')
@app.route('/')
def index():
    return render_template('index.html')


@app.route("/authenticate")
def authenticate():
    auth_url = auth_app.authorize_url()
    return redirect(auth_url)


@app.route('/auth', methods=['GET', 'POST'])
def auth():
    error = request.args.get('error', '')
    if error:
        return "Error: " + error

    if request.method == 'GET':
        auth_code = request.args.get('code')
        token_dict = auth_app.get_token(auth_code)
        session['access_token'] = token_dict['access_token']
        session['expires_in'] = token_dict['expires_in']
        content_token = "access_token: {} </br> token_type: {} </br> expires_in: {} </br> refresh_token: {}".format(
            token_dict['access_token'], token_dict['token_type'], str(token_dict['expires_in']),
            token_dict['refresh_token']
        )
        return render_template('index.html', content=Markup(content_token))


@app.route('/user_info', methods=['GET', 'POST'])
def user_info():
    if 'access_token' not in session:
        error = 'You are not authenticated!'
        return render_template('index.html', error=error)

    error = request.args.get('error', '')
    if error:
        return "Error: " + error

    user_info = auth_app.get_user_info(session['access_token'])
    content_user = 'username: {} </br> email: {}'.format(user_info['displayName'], user_info['email'])
    roles = user_info['roles']
    session['roles'] = []
    for role in roles:
        session['roles'].append(str(role['name']))
    return render_template('index.html', content=Markup(content_user + '</br> roles: ' + str(session['roles'])))


@app.route("/username", methods=['GET'])
def username():
    if request.args.get('username') == '':
        error = 'Fill the name field first!'
        return render_template('index.html', error=error)
    headers = {"X-Auth-Token": session['access_token']}
    response = requests.get(auth_app.proxy_address + "service1/" + request.args.get('username'), headers=headers)
    return render_template('index.html', content=response.text)


@app.route("/list", methods=['GET'])
def list():
    headers = {"X-Auth-Token": session['access_token'], "Authorization": "bearer " + session['access_token']}
    response = requests.get(auth_app.proxy_address + "service2/list", headers=headers)
    return render_template('index.html', content=response.text)


@app.route("/add", methods=['GET'])
def add():
    if request.args.get('name') == '':
        error = 'Fill the name field first!'
        return render_template('index.html', error=error)
    headers = {'X-Auth-Token': session['access_token']}
    response = requests.get(auth_app.proxy_address + "service2/add/" + request.args.get('name'), headers=headers)
    return render_template('index.html', content=response.text)


if __name__ == '__main__':
    app.run(port=5050)
