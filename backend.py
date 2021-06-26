# Save the client secret as SOMEBODY_CLIP_THAT_CLIENT_SECRET, then
# `export SOMEBODY_CLIP_THAT_CLIENT_SECRET`
import requests
import os
import json
import sys, getopt

def main(argv):
    '''
    Step 1: Get the oauth token
    '''

    client_id = "iliayvc79au07dbm3hk21a0f1y730k"
    client_secret = os.environ["SOMEBODY_CLIP_THAT_CLIENT_SECRET"]

    url = "https://id.twitch.tv/oauth2/token"
    params = {"client_id": client_id,
              "client_secret": "wk0uojpj2bonyjgure2mgqjieijphz",
              "grant_type": "client_credentials",
              "scope": "clips:edit user:read:email"}
    x = requests.post(url,params=params)


    res = json.loads(x.text)
    access_token =  res["access_token"]
    print("access token: ", access_token)

    headers = {"Authorization": "Bearer " + access_token,
               "Client-Id": client_id}

    # Step 2: Get the broadcaster id from username. username should come from argv instead of hardcoded
    username = "vgbootcamp"
    url = "https://api.twitch.tv/helix/users"
    params = {"login":username}
    x = requests.get(url,params=params, headers=headers)
    res = json.loads(x.text)
    print(res)
    broadcaster_id = res["data"][0]["id"]
    print("broadcaster id:", broadcaster_id)

    '''
    Step 3: use the token to make "create clip requests"
    curl -X POST 'https://api.twitch.tv/helix/clips?broadcaster_id=44322889' \
    -H 'Authorization: Bearer cfabdegwdoklmawdzdo98xt2fo512y' \
    -H 'Client-Id: uo6dggojyb8d6soh92zknwmi5ej1q2'
    https://dev.twitch.tv/docs/api/reference
    Returns id and url
    '''
    url = "https://api.twitch.tv/helix/clips"
    params = {"broadcaster_id", broadcaster_id}
    x = requests.post(url,params=params, headers=headers)




    '''
    Step 4: "Get the created clip"
    GET https://api.twitch.tv/helix/clips

    query param: id
    '''

if __name__ == "__main__":
    main(sys.argv[1:])
