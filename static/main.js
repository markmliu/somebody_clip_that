var recognition = new webkitSpeechRecognition();
var access_token = null;
var broadcaster_id = null;

// TODO can this be passed from server so there's just one place it lives?
const CLIENT_ID = "iliayvc79au07dbm3hk21a0f1y730k";

// just for debugging
var response_info;

window.onload = function() {
    initSpeechRecognition();
    access_token = getCookie("access_token");
}

function initSpeechRecognition() {
    recognition.continuous = true;
    recognition.onresult = function (event) {
        let results = (event.results);
        let new_speech = results[results.length - 1][0].transcript;
        console.log(new_speech);
        if (new_speech.tolowercase().includes("somebody clip that")) {
            onClipRequested();
        }
    };
    recognition.onnomatch = function (event) {
        console.log("no match");
    };
    recognition.onerror = function (event) {
        console.log("error");
    };
}

function startSpeechRecognition() {
    recognition.start();
    getBroadcastId();
}

function stopSpeechRecognition() {
    recognition.stop();
}

function getStreamUser() {
    return document.getElementById("stream_user").value;
}

function onClipRequested() {
    console.log("onClipRequested");
    // TODO create clip with Twitch API
}

function getBroadcastId() {
    $.get({
          url: "https://api.twitch.tv/helix/users",
          headers: {
              "Authorization": "Bearer " + access_token,
              "Client-Id": CLIENT_ID
          },
          data: {"login": getStreamUser() },
    }).done(function(response) {
        response_info = response;
        console.log("getBroadcastId done. response_info=" + response_info);
        if (response.data.length == 0) {
            console.log("bad streamer username");
            stopSpeechRecognition();
        } else {
            response_info = response;
            broadcaster_id = response.data[0].id
            //description: "Grandmaster Hikaru Nakamura, 5-time United States Chess Champion "
            //display_name: "GMHikaru"
            //offline_image_url
            //profile_image_url
        }
    });
}

function createClip() {
    $.post({
          url: "https://api.twitch.tv/helix/clips",
          headers: {
              "Authorization": "Bearer " + access_token,
              "Client-Id": CLIENT_ID
          },
          data: {"broadcaster_id": broadcaster_id },
    }).done(function(response) {
        response_info = response;
        console.log("createClip done. response_info=" + response_info);
    });
}

function getCookie(cname) {
    let name = cname + "=";
    let decoded_cookie = decodeURIComponent(document.cookie);
    let ca = decoded_cookie.split(';');
    for(let i = 0; i <ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}
