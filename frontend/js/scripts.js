var request = new XMLHttpRequest()

// https://developer.mozilla.org/en-US/docs/Web/API/File_System_Access_API

function Add () {
    request.open("POST", "http://127.0.0.1:8000/add", true)
    request.setRequestHeader("accept", "application/json")
    request.setRequestHeader("Content-Type", "application/json")
    var newFilesFromElement = document.getElementById("newFilesToQueue").files;
    console.log(newFilesFromElement)
    var file;
    var newFiles = [];
    for (var i = 0; i < newFilesFromElement.length; i++) {
        file = newFilesFromElement[i];
        console.log(file.name)
        newFiles.push(file.name);
    }
    console.log(newFiles)
    var dict = {};
    dict["files"] = newFiles;
    var json = JSON.stringify(dict);
    request.send(json)
}

let fileHandle;
const pickerOpts = {
    types: [
        {
            description: 'Videos'
        },
    ],
    excludeAcceptAllOption: true,
    multiple: true
    };

async function getFiles() {
    var fileHandle
    fileHandles = await window.showOpenFilePicker(pickerOpts);
    console.log(fileHandle)
    for (var i = 0; i < fileHandles.length; i++) {
        var fileData = await fileHandles[i].getFile();
        console.log(fileData.name)
        }
}

function upload() {
    let videos = document.getElementById("newFilesToQueue").files;
    let req = new XMLHttpRequest();
    let formData = new FormData();
    formData.append("videos", videos);

    console.log(videos)
    console.log(formData)

    //req.open("POST", "/upload");
    //req.send(formData);
}




function Queue () {
    request.open("GET", "http://127.0.0.1:8000/queue", true)
    request.onload = function () {

      var data = JSON.parse(this.response)

      if (request.status >= 200 && request.status < 400) {
        data.forEach((movie) => {
          console.log(movie.title)
        })
      } else {
        console.log('error')
      }
    }
    request.send()
}
