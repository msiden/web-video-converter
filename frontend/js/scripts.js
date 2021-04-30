const URL = "http://127.0.0.1:8000/"
var request = new XMLHttpRequest()

function Add () {
    request.open("POST", URL + "add", true)
    request.setRequestHeader("accept", "application/json")
    request.setRequestHeader("Content-Type", "application/json")
    var newFilesFromElement = document.getElementById("newFilesToQueue").files;
    var file;
    var newFiles = [];
    for (var i = 0; i < newFilesFromElement.length; i++) {
        file = newFilesFromElement[i];
        newFiles.push(file.name);
    }
    var dict = {};
    dict["files"] = newFiles;
    var json = JSON.stringify(dict);
    request.send(json)
}

function Upload() {
    let formData = new FormData();
    var no_of_files = document.getElementById('filesToUpload').files.length;
    for (var i = 0; i < no_of_files; i++) {
        formData.append("files", document.getElementById('filesToUpload').files[i]);
    }
    request.open("POST", URL + "upload");
    request.send(formData);
}

function SetBitrate() {

}

function ProcessQueue() {

}

function DownloadFiles() {

}