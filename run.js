
const startSessionButton = document.getElementById('startSession');
const stopSessionButton = document.getElementById('stopSession');

startSessionButton.addEventListener('click', () => {
    // Send a POST request to the backend to start the session
    fetch('/start_session', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => console.log(data));
});

stopSessionButton.addEventListener('click', () => {
    // Send a POST request to the backend to stop the session
    fetch('/stop_session', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => console.log(data));
});

// Set up an observer to listen for phone detection updates
const observer = new IntersectionObserver((entries) => {
    if (entries[0].isIntersecting) {
        // Send a POST request to the backend to get the phone detection status
        fetch('/phone_detected', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.phone_detected) {
                // Use the alert function to display a message
                playAlert();
            }
        });
    }
}, {
    root: null,
    rootMargin: '0px',
    threshold: 1.0
});

observer.observe(document.getElementById('phoneDetectionElement'));
