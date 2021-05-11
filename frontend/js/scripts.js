const COOKIE = document.cookie.replace("uuid=", "")
const URL = window.location.href
const USER_FILES = URL + "user_files/" + COOKIE
const LINK = USER_FILES + "/completed/converted_files.zip"
var request = new XMLHttpRequest()
var res


function Upload() {
    document.getElementById("statusText").innerHTML = "Uploading files...";
    let formData = new FormData();
    var no_of_files = document.getElementById('filesToUpload').files.length;
    for (var i = 0; i < no_of_files; i++) {
        formData.append("files", document.getElementById('filesToUpload').files[i]);
    }

    request.onreadystatechange = function() {
        if (request.readyState === 4) {
            document.getElementById("statusText").innerHTML = "";
            document.getElementById("actionButton").style = "";
            document.getElementById("actionButton").onclick = function() { ProcessQueue(); }
        }
    }

    request.open("POST", URL + "upload");
    request.send(formData);
}

function SetBitrate() {
    var newBitrate = document.getElementById("bitrateVal").value;
    request.open("PUT", URL + "set_bitrate");
    request.send(JSON.stringify({"bitrate": newBitrate}));
}

function ProcessQueue() {
    document.getElementById("actionButton").style = "display:none;";
    document.getElementById("statusText").innerHTML = "Processing... This may take a while so please be patient.";
    request.onreadystatechange = function() {
        if (request.readyState === 4) {
            document.getElementById("statusText").innerHTML = "";
            document.getElementById("actionButton").style = "";
            document.getElementById("actionButton").onclick = function() { open(LINK) }
            document.getElementById("actionButton").innerHTML = "Download converted files";
        }
    }
    request.open("POST", URL + "process");
    request.send(null);
}
