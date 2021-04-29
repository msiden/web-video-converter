var request = new XMLHttpRequest()

function Add () {
    request.open("POST", "http://127.0.0.1:8000/add", true)
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

function upload() {
    let videos = document.getElementById("filesToUpload").files[0];
    let formData = new FormData();
    formData.append("files", videos);

    //console.log(videos)
    //console.log(formData);

    //var file;
    //var newFiles = [];
    //for (var i = 0; i < videos.length; i++) {
    //    file = videos[i];
    //    newFiles.push(file);
    //    console.log(file)
    //}
    //console.log(newFiles)
    //formData.append("files", newFiles);
    //formData.append("files", newFiles);

    request.open("POST", "http://127.0.0.1:8000/upload");
    //request.setRequestHeader("accept", "application/json")
    //request.setRequestHeader("Content-Type", "multipart/form-data")
    //request.setRequestHeader("Content-Type", "multipart/undefined")
    request.send(formData);
    //request.send(newFiles);
    //request.send(videos);

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
