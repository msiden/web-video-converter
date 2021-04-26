var request = new XMLHttpRequest()


function Add () {
    request.open("POST", "http://127.0.0.1:8000/add", true)
    request.setRequestHeader("accept", "application/json")
    request.setRequestHeader("Content-Type", "application/json")
    var newFilesToQueue = document.getElementById("newFilesToQueue").value;
    var dict = {};
    dict["files"] = [newFilesToQueue];
    var json = JSON.stringify(dict);
    request.send(json)
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
