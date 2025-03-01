import cv2
import cvlib as cv
from cvlib.object_detection import draw_bbox

import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

video = cv2.VideoCapture(0)

labels = []

while True:
    ret, frame = video.read()
    bbox, label, conf = cv.detect_common_objects(frame)
    #conf -- confidence
    # label -- what it detects it as
    # bbox -- collection of 4 points?
    output_image = draw_bbox(frame, bbox, label, conf)

    cv2.imshow("Object Detetion", output_image)

    for obj in label:
        if obj in labels:
            pass
        else:
            labels.append(obj)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        print(labels)
        break

cv2.destroyAllWindows()
