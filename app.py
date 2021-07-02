from flask import Flask
from flask import request
from flask import render_template
from flask import make_response
import os
import json
import requests

CLIENT_ID = "iliayvc79au07dbm3hk21a0f1y730k"
#TODO this url needs to be the server's URL, instead of hardcoded as localhost
REDIRECT_URL = "http://localhost:5000/login"
CLIENT_SECRET = ""
SCOPE = "clips:edit user:read:email"

def get_login_link():
    # read client secret from env variable
    global CLIENT_SECRET
    CLIENT_SECRET = os.environ["SOMEBODY_CLIP_THAT_CLIENT_SECRET"]
    print ("client secret: ", CLIENT_SECRET)

    login_url = "https://id.twitch.tv/oauth2/authorize?client_id="+CLIENT_ID+"&redirect_uri="+REDIRECT_URL+"&response_type=code&scope="+SCOPE
    return login_url


app = Flask(__name__, template_folder="templates")

def get_access_token(code, redirect_url):
    url = "https://id.twitch.tv/oauth2/token"
    params = {"client_id":CLIENT_ID,
              "client_secret":CLIENT_SECRET,
              "code":code,
              "grant_type":"authorization_code",
              "redirect_uri":redirect_url}
    x = requests.post(url,params=params)

    print(x.json())
    access_token = x.json().get("access_token", "")
    print("access token: ", access_token)
    return access_token

@app.route("/")
def index():
    access_token = request.cookies.get('access_token')
    if access_token is None:
        return render_template('index.html', logged_in=False, login_link=get_login_link())
    else:
        return render_template('index.html', logged_in=True, client_id=CLIENT_ID)

@app.route("/login")
def login():
    code = request.args.get('code')
    url = request.url.split('?')[0]
    print("code in url params:", code)
    print("url:", url)

    access_token = get_access_token(code, url)
    if access_token:
        resp = make_response(render_template('index.html', logged_in=True, client_id=CLIENT_ID))
        resp.set_cookie('access_token', get_access_token(code, url))
        return resp
    else:
        return render_template('index.html', logged_in=False, error=True, client_id=CLIENT_ID)


if __name__ == "__main__":
    # read client secret from env variable
    global CLIENT_SECRET
    CLIENT_SECRET = os.environ["SOMEBODY_CLIP_THAT_CLIENT_SECRET"]
    print("client secret: ", CLIENT_SECRET)

    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    server_port = os.environ.get('PORT', '8080')
    app.run(host='0.0.0.0', port=server_port)
