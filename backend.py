# Save the client secret as SOMEBODY_CLIP_THAT_CLIENT_SECRET, then
# `export SOMEBODY_CLIP_THAT_CLIENT_SECRET`

from flask import Flask
from flask import request
import webbrowser
import os
import json
import requests

client_id = "iliayvc79au07dbm3hk21a0f1y730k"
redirect_url = "http://localhost:5000/login"

client_secret = ""
access_token = ""

scope = "clips:edit user:read:email"

def startup():
  print('MyFlaskApp is starting up!')
  # read client secret from env variable
  global client_secret
  client_secret = os.environ["SOMEBODY_CLIP_THAT_CLIENT_SECRET"]
  print ("client secret: ", client_secret)

  login_url = "https://id.twitch.tv/oauth2/authorize?client_id="+client_id+"&redirect_uri="+redirect_url+"&response_type=code&scope="+scope
  webbrowser.open_new_tab(login_url)

def trade_code_for_token(code):
    url = "https://id.twitch.tv/oauth2/token"
    params = {"client_id":client_id,
              "client_secret":client_secret,
              "code":code,
              "grant_type":"authorization_code",
              "redirect_uri":redirect_url}
    x = requests.post(url,params=params)

    print(x.json())
    global access_token
    access_token = x.json()["access_token"]
    print("access token: ", access_token)

def get_broadcaster_id(username):
    headers = {"Authorization": "Bearer " + access_token,
               "Client-Id": client_id}
    url = "https://api.twitch.tv/helix/users"
    params = {"login":username}
    x = requests.get(url,params=params, headers=headers)
    res = json.loads(x.text)
    print(res)
    return res["data"][0]["id"]

def create_clip(broadcaster_id):
    headers = {"Authorization": "Bearer " + access_token,
               "Client-Id": client_id}
    url = "https://api.twitch.tv/helix/clips"
    params = {"broadcaster_id":broadcaster_id}
    x = requests.post(url,params=params,headers=headers)
    return x.json()["data"][0]["id"]



class MyFlaskApp(Flask):
  def run(self, host=None, port=None, debug=None, load_dotenv=True, **options):
    if not self.debug or os.getenv('WERKZEUG_RUN_MAIN') == 'true':
      with self.app_context():
        startup()
    super(MyFlaskApp, self).run(host=host, port=port, debug=debug, load_dotenv=load_dotenv, **options)


app = MyFlaskApp(__name__)
app.run()

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/login")
def login():
    code = request.args.get('code')
    print("code in url params:", code)
    trade_code_for_token(code)
    return "Code received"

@app.route("/clip")
def clip():
    username = "vgbootcamp"
    broadcaster_id = get_broadcaster_id(username)
    print("broadcaster id: ", broadcaster_id)
    clip_id = create_clip(broadcaster_id)
    print("created clip with id: ", clip_id)
    return "Created clip"
