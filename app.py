from flask import Flask
from flask import request
from flask import render_template
from flask import make_response
import os
import json
import requests

CLIENT_ID = "iliayvc79au07dbm3hk21a0f1y730k"
#TODO this url needs to be the server's URL, instead of hardcoded as localhost
REDIRECT_URL = "https://somebodyclipthat-nekfxpjbea-uw.a.run.app/login"
SCOPE = "clips:edit user:read:email"
CLIENT_SECRET = ""

def get_login_link():
    return "https://id.twitch.tv/oauth2/authorize?client_id="+CLIENT_ID+"&redirect_uri="+REDIRECT_URL+"&response_type=code&scope="+SCOPE

app = Flask(__name__, template_folder="templates")

def get_access_token(code, redirect_url):
    print("redirect_url =", redirect_url)
    print("REDIRECT_URL =", REDIRECT_URL)
    url = "https://id.twitch.tv/oauth2/token"
    params = {"client_id":CLIENT_ID,
              "client_secret":CLIENT_SECRET,
              "code":code,
              "grant_type":"authorization_code",
              "redirect_uri":REDIRECT_URL}
    x = requests.post(url,params=params)

    access_token = x.json().get("access_token", "")
    return access_token

@app.route("/")
def index():
    access_token = request.cookies.get('access_token')
    redirect_url = request.url.split('?')[0]
    print("redirect_url =", redirect_url)
    if access_token is None:
        return render_template('index.html', logged_in=False, login_link=get_login_link())
    else:
        return render_template('index.html', logged_in=True, client_id=CLIENT_ID)

@app.route("/login")
def login():
    code = request.args.get('code')
    redirect_url = request.url.split('?')[0]
    access_token = get_access_token(code, redirect_url)
    if access_token:
        resp = make_response(render_template('index.html', logged_in=True, client_id=CLIENT_ID))
        resp.set_cookie('access_token', access_token)
        return resp
    else:
        return render_template('index.html', logged_in=False, error=True, client_id=CLIENT_ID)


if __name__ == "__main__":
    # read client secret from env variable
    CLIENT_SECRET = os.environ["SOMEBODY_CLIP_THAT_CLIENT_SECRET"]
    print("client secret: ", CLIENT_SECRET)

    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    server_port = os.environ.get('PORT', '8080')
    app.run(debug=True, host='0.0.0.0', port=server_port)
