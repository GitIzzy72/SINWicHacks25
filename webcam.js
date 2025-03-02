

let video = document.querySelector("#webcam");
if (navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(function (stream) {
            video.srcObject = stream;
        })
        .catch(function (err0) {
            console.log("Something went wrong!");
        });
}
else {
    console.log("getUserMedia() is not supported in your browser");
}




