import cv2
import cvlib as cv
from cvlib.object_detection import draw_bbox
import time
from playsound import playsound

import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# to do: 
# fix global variable bull shit
# patch it up to flask

longestTime = 0
totalPhoneDistractions = 0
targetObject = "cell phone"
minConfidence = .45
phoneFoundRatio = .6



def newMaxTime(time):
    global longestTime

    if(time>longestTime):
        longestTime=time
        print("new longest time "+str(longestTime))

def main(): 
    global targetObject
    global minConfidence
    global phoneFoundRatio
    global longestTime
    global totalPhoneDistractions

    timerStart = time.time()
    timeInQuestion = time.time() #The last time we are certain they weren't on their phone
    storedTime = 0 

    nowCounting = False # when true, increment totalFound
    totalFound = 0 #number of frames a phone has been counted
    framesPassed = 0
    denominatorFrames = 20

    phoneInView=False


    video = cv2.VideoCapture(0)

    while True:
        ret, frame = video.read()
        bbox, label, conf = cv.detect_common_objects(frame)
        #conf -- confidence
        # label -- what it detects it as
        # bbox -- collection of 4 points?

        output_image = draw_bbox(frame, bbox, label, conf, write_conf=True)
        cv2.imshow("Object Detetion", output_image)
        
        # cv2.imshow("Object Detetion", frame)

        currentFramePhonePresent = (targetObject in label) #true when phone is in screen on this frame
        confidence = 0
        if(currentFramePhonePresent):
            confidence=conf[label.index(targetObject)]

        if(nowCounting):
            framesPassed+=1
            print(str(framesPassed)+", phone present: "+str(currentFramePhonePresent))

            if(currentFramePhonePresent):
                if(confidence>minConfidence):
                    totalFound+=1

        # phone presence in this frame does not match state and counting isn't happening
        if( not (currentFramePhonePresent==phoneInView or nowCounting) ):
            #if you're testing for phone leaving set the potential start time to when this process begins
            storedTime = time.time()
            framesPassed = 0
            totalFound = 0
            nowCounting=True

        if(framesPassed==denominatorFrames): 
            print("interval reached")
            print("Toal found "+str(totalFound))
            print("Ratio: "+str(totalFound/denominatorFrames))

            #phoneFound is true if the ratio of found frames is above the threshold
            countPhoneFound = (totalFound/denominatorFrames)>=phoneFoundRatio
            framesPassed = 0
            totalFound = 0
            phonelessTime = 0

            if(countPhoneFound and not phoneInView): 
                #stop timer and save timec
                phonelessTime = storedTime - timerStart
                newMaxTime(phonelessTime)

            if(not countPhoneFound and phoneInView):
                #new start time is where this began the count
                timerStart = storedTime

            phoneInView = countPhoneFound

            if(phoneInView):
                phoneConfirmed(phonelessTime)
                print("Current state -- phone in view")
            else:
                phoneLeftScreen()
                print("Current state -- no phone")
            nowCounting=False

            
        
        if cv2.waitKey(1) & 0xFF == ord("q"):
            print("Your longest time without a phone was "+longestTime+" seconds")
            print("You picked up your phone "+totalPhoneDistractions+" times")
            break

    cv2.destroyAllWindows()

def phoneLeftScreen():
    print("You put your phone down!")

def phoneConfirmed(timeOff):
    global totalPhoneDistractions
    totalPhoneDistractions +=1
    print("You're on your phone!")
    print("You were off your phone for "+timeOff+" seconds")

def getLongestTime():
    global longestTime
    return longestTime

def getTotalPickups():
    global totalPhoneDistractions
    return totalPhoneDistractions

main()