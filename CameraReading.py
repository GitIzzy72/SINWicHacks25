import cv2
# import cvlib as cv
# from cvlib.object_detection import draw_bbox
import time
import sys
import argparse
import glob

import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import numpy as np
from ultralytics import YOLO

parser = argparse.ArgumentParser()
parser.add_argument('--model', help='Path to YOLO model file (example: "runs/detect/train/weights/best.pt")',
                    required=True)

args = parser.parse_args()
model_path = args.model

# Load the model into memory and get labemap
model = YOLO(model_path, task='detect')
labels = model.names

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


        # Run inference on frame
        results = model(frame, verbose=False)

        # Extract results
        detections = results[0].boxes

        # Initialize variable for basic object counting example
        object_count = 0

        # bbox, label, conf = cv.detect_common_objects(frame)
        #conf -- confidence
        # label -- what it detects it as
        # bbox -- collection of 4 points?

        # output_image = draw_bbox(frame, bbox, label, conf, write_conf=True)
        
        
        
         # Go through each detection and get bbox coords, confidence, and class
        for i in range(len(detections)):

            # Get bounding box coordinates
            # Ultralytics returns results in Tensor format, which have to be converted to a regular Python array
            xyxy_tensor = detections[i].xyxy.cpu() # Detections in Tensor format in CPU memory
            xyxy = xyxy_tensor.numpy().squeeze() # Convert tensors to Numpy array
            xmin, ymin, xmax, ymax = xyxy.astype(int) # Extract individual coordinates and convert to int

            # Get bounding box class ID and name
            classidx = int(detections[i].cls.item())
            classname = labels[classidx]

            # Get bounding box confidence
            conf = detections[i].conf.item()

            # Draw box if confidence threshold is high enough
            if conf > 0.5:

                color = bbox_colors[classidx % 10]
                cv2.rectangle(frame, (xmin,ymin), (xmax,ymax), color, 2)

                label = f'{classname}: {int(conf*100)}%'
                labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1) # Get font size
                label_ymin = max(ymin, labelSize[1] + 10) # Make sure not to draw label too close to top of window
                cv2.rectangle(frame, (xmin, label_ymin-labelSize[1]-10), (xmin+labelSize[0], label_ymin+baseLine-10), color, cv2.FILLED) # Draw white box to put label text in
                cv2.putText(frame, label, (xmin, label_ymin-7), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1) # Draw label text

                # Basic example: count the number of objects in the image
                object_count = object_count + 1

        
        
        # cv2.putText(frame, f'FPS: {avg_frame_rate:0.2f}', (10,20), cv2.FONT_HERSHEY_SIMPLEX, .7, (0,255,255), 2) # Draw framerate
        
        
        cv2.imshow("Object Detetion", frame)
        
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

            if(countPhoneFound and not phoneInView): 
                #stop timer and save timec
                phonelessTime = storedTime - timerStart
                newMaxTime(phonelessTime)

            if(not countPhoneFound and phoneInView):
                #new start time is where this began the count
                timerStart = storedTime

            phoneInView = countPhoneFound

            if(phoneInView):
                phoneConfirmed()
                print("Current state -- phone in view")
            else:
                print("Current state -- no phone")
            nowCounting=False

            
        
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cv2.destroyAllWindows()


def phoneConfirmed():
    totalPhoneDistractions +=1
    print("Goober!!")

def getLongestTime():
    global longestTime
    return longestTime

def getTotalPickups():
    global totalPhoneDistractions
    return totalPhoneDistractions

main()