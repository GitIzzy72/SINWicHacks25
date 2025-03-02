import CameraReading
from flask import Flask, request, jsonify

app = Flask(__name__)

totalPickups = 0
longestTime = 0

@app.route('/startSession', methods=['POST'])
def startSession():
    '''global totalPickups
    global longestTime
    totalPickups = CameraReading.getTotalPickups()
    longestTime = CameraReading.getLongestTime()'''
    # Start the CV and begin looking for a phone
    # This will run constantly until stop_session is called
    return jsonify({'message': 'Session started'})

@app.route('/stopSession', methods=['POST'])
def stopSession():
    '''global totalPickups
    global longestTime
    totalPickups = CameraReading.getTotalPickups()
    longestTime = CameraReading.getLongestTime()'''
    # Stop the CV
    return jsonify({'message': 'Session stopped'})

@app.route('/phone_detected', methods=['POST'])
def phone_detected():
    data = request.get_json()
    if data["phone_detected"]:
        print("Phone detected!")
        # Do something when a phone is detected
    else:
        print("No phone detected!")
        # Do something when no phone is detected
    return jsonify({"phone_detected": phone_detected})


if __name__=='__main__':
    CameraReading.main()
    app.run()