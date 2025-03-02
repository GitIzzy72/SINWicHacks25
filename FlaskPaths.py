import CameraReading
from flask import Flask

app = Flask(__name__)

totalPickups = 0
longestTime = 0

if __name__=='__main__':
    CameraReading.main()
    app.run()