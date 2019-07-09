import numpy as np
import os
from glob import glob
import scipy.io as sio
from skimage.io import imread, imsave
from time import time
import cv2

from api import PRN
from utils.write import write_obj_with_colors
from utils.render_app import get_depth_image
from utils.render import get_depth_buffer

def bbox2(img):
    rows = np.any(img, axis=1)
    cols = np.any(img, axis=0)
    rmin, rmax = np.where(rows)[0][[0, -1]]
    cmin, cmax = np.where(cols)[0][[0, -1]]

    return rmin, rmax, cmin, cmax

# ---- init PRN
os.environ['CUDA_VISIBLE_DEVICES'] = '3' # GPU number, -1 for CPU
prn = PRN(is_dlib = True) 


# ------------- load data
image_folder = 'resized_image/'
save_folder = 'depth_groundTruth/'
if not os.path.exists(save_folder):
    os.mkdir(save_folder)

types = ('*.jpg', '*.png')
image_path_list= []
for files in types:
    image_path_list.extend(glob(os.path.join(image_folder, files)))
total_num = len(image_path_list)

for i, image_path in enumerate(image_path_list):
    # read image
    image = imread(image_path)

    # the core: regress position map    
    if 'AFLW2000' in image_path:
        mat_path = image_path.replace('jpg', 'mat')
        info = sio.loadmat(mat_path)
        kpt = info['pt3d_68']
        pos = prn.process(image, kpt) # kpt information is only used for detecting face and cropping image
    else:
        pos = prn.process(image) # use dlib to detect face

    vertices = prn.get_vertices(pos) # get 3D vertices
    triangles = prn.triangles # get triangles


    depth_buffer, depth_map = get_depth_image(vertices, triangles, 500, 500) # get depth buffer and depth map with size (500,500)
    depth_buffer = np.array(depth_buffer)
    rmin, rmax, cmin, cmax = bbox2(depth_buffer) # centralize the depth map
    depth_buffer = depth_buffer[rmin:rmax,cmin:cmax]
    #depth_buffer = cv2.resize(depth_buffer,(32,32),interpolation=cv2.INTER_CUBIC)
    name = image_path.strip().split('/')[-1][:-4]
    imsave((os.path.join(save_folder, name + '.jpg')), depth_buffer) # save depth map
    np.savetxt(os.path.join(save_folder, name + '.txt'), depth_buffer) # save depth matrix