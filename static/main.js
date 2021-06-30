var recognition = new webkitSpeechRecognition();
var access_token = null;

window.onload = function() {
    initspeechrecognition();
    access_token = getCookie("access_token");
    document.getElementById("access_token").textContent = access_token;
}

function initspeechrecognition() {
    recognition.continuous = true;
    recognition.onresult = function (event) {
        let results = (event.results);
        let newspeech = results[results.length - 1][0].transcript;
        console.log(newspeech);
        if (newspeech.tolowercase().includes("somebody clip that")) {
            oncliprequested();
        }
    };
    recognition.onnomatch = function (event) {
        console.log("no match");
    };
    recognition.onerror = function (event) {
        console.log("error");
    };
}

function startspeechrecognition() {
    recognition.start();
}

function getstreamuser() {
    return document.getelementbyid("stream_user").value;
}

function oncliprequested() {
    console.log("oncliprequested");
    // TODO convert stream_user into broadcast_id with Twitch API
    // TODO create clip with Twitch API
}

function getCookie(cname) {
    let name = cname + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';');
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
