import cv2
import os
import numpy as np
import matplotlib.pyplot as plt
from glob import glob
from skin_detector import face_detect, resize_image

frame_folder = './train_image/'
save_folder = './resized_image/'

if not os.path.exists(save_folder):
    os.mkdir(save_folder)

types = ('*.jpg', '*.png')
image_path_list= []
for files in types:
    image_path_list.extend(glob(os.path.join(frame_folder, files)))
total_num = len(image_path_list)

rppg_forehead = []
rppg_left = []
for i, image_path in enumerate(image_path_list):
    # read image
    image = cv2.imread(image_path)
    face = face_detect(image)
    newimage = resize_image(face, (256,256))
    filename = os.path.basename(image_path)
    cv2.imwrite(save_folder+'resized_'+filename, newimage)
    