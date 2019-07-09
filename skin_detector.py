import cv2
import numpy as np
import os
from glob import glob

# ----- use haarcascade frontface detector to detect face region
def face_detect(skin):
    path = os.path.abspath('haarcascade_frontalface_alt.xml')
    hc=cv2.CascadeClassifier(path)
    faces=hc.detectMultiScale(skin)

    for face in faces:

        global imgROI
        imgROI = skin[face[1]:face[1]+face[3],face[0]:face[0]+face[2]]

    return imgROI

def resize_image(image, newsize):
    newimage = cv2.resize(image, newsize, interpolation=cv2.INTER_AREA)
    return newimage