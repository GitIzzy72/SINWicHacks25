function wait(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}
  
function playAlert() {
    document.getElementById('notification').play()
    window.alert("sometext");
}