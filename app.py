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

app = Flask(__name__, template_folder="templates")

def get_login_link():
  # read client secret from env variable
  global CLIENT_SECRET
  CLIENT_SECRET = os.environ["SOMEBODY_CLIP_THAT_CLIENT_SECRET"]
  print ("client secret: ", CLIENT_SECRET)

  login_url = "https://id.twitch.tv/oauth2/authorize?client_id="+CLIENT_ID+"&redirect_uri="+REDIRECT_URL+"&response_type=code&scope="+SCOPE
  return login_url

def get_access_token(code):
    url = "https://id.twitch.tv/oauth2/token"
    params = {"client_id":CLIENT_ID,
              "client_secret":CLIENT_SECRET,
              "code":code,
              "grant_type":"authorization_code",
              "redirect_uri":REDIRECT_URL}
    x = requests.post(url,params=params)

    print(x.json())
    access_token = x.json()["access_token"]
    print("access token: ", access_token)
    return access_token

#TODO move this into client
def get_broadcaster_id(username):
    access_token = "get this from the client"
    headers = {"Authorization": "Bearer " + access_token,
               "Client-Id": CLIENT_ID}
    url = "https://api.twitch.tv/helix/users"
    params = {"login":username}
    x = requests.get(url,params=params, headers=headers)
    res = json.loads(x.text)
    print(res)
    return res["data"][0]["id"]

#TODO move this into client
def create_clip(broadcaster_id):
    access_token = "get this from the client"
    headers = {"Authorization": "Bearer " + access_token,
               "Client-Id": CLIENT_ID}
    url = "https://api.twitch.tv/helix/clips"
    params = {"broadcaster_id":broadcaster_id}
    x = requests.post(url,params=params,headers=headers)
    return x.json()["data"][0]["id"]

@app.route("/")
def index():
    access_token = request.cookies.get('access_token')
    if access_token is None:
        return render_template('index.html', logged_in=False, login_link=get_login_link())
    else:
        return render_template('index.html', logged_in=True)

@app.route("/login")
def login():
    code = request.args.get('code')
    print("code in url params:", code)

    resp = make_response(render_template('index.html', logged_in=True))
    resp.set_cookie('access_token', get_access_token(code))
    return resp

    #return render_template('index.html', logged_in=True, access_token=get_access_token(code))

#TODO this endpoint can be removed
@app.route("/clip")
def clip():
    username = "vgbootcamp"
    broadcaster_id = get_broadcaster_id(username)
    print("broadcaster id: ", broadcaster_id)
    clip_id = create_clip(broadcaster_id)
    print("created clip with id: ", clip_id)
    return "Created clip"

if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True, host='0.0.0.0')
