import scipy.io as sio
from utils.rotate_vertices import frontalize
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from utils.render_app import get_depth_image
from skimage.io import imread, imsave

data = sio.loadmat('image00002_mesh.mat')
vertices = data['vertices']
triangles = data['triangles']
front_v = frontalize(vertices)
print(vertices)
print(front_v)

