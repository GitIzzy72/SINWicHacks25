import cv2
import cvlib as cv
from cvlib.object_detection import draw_bbox
import time

import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

def current_milli_time():
    return round(time.time() * 1000)

def main(): 
    targetObject = "cell phone"
    minConfidence = .85
    innocenceLimit = 5 # amount of frames before an sighting is terminate

    firstSighting = 0 # time when phone sighting first began 
    suspicion = False # when true it means that there was a phone sighting recently

    phoneDissapeared = 0 
    innocenceTrial = False
    notAFalseAlarm = 1

    video = cv2.VideoCapture(0)

    while True:
        ret, frame = video.read()
        bbox, label, conf = cv.detect_common_objects(frame)
        #conf -- confidence
        # label -- what it detects it as
        # bbox -- collection of 4 points?
        output_image = draw_bbox(frame, bbox, label, conf, write_conf=True)

        cv2.imshow("Object Detetion", output_image)

        #check if it sees cellphone
        #check cellphones confidence metric
        #check if the program believes this is a continuous viewing of the phone --suspicion
        #is the distance from beginning of suspicion more than 


        if ((targetObject in label)):
            if(suspicion and ((time.time()-firstSighting)>innocenceLimit)):
                phoneConfirmed()

            if(not suspicion):
                suspicion=True
                firstSighting = time.time()
        else:
            if(suspicion):
                innocenceTrial = True
                phoneDissapeared = time.time()
            
            if(innocenceTrial and (time.time()-phoneDissapeared)>notAFalseAlarm):
                suspicion=False
                print("Phone gone")
            



        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cv2.destroyAllWindows()

def phoneConfirmed():
    print("Goober!!")

main()