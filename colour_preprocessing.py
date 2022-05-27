# ------- IMPORT --------------

from sklearn.cluster import KMeans
from scipy.spatial import KDTree
import numpy as np
import cv2
import glob
import os
import csv
import ast

    
# ------- FUNCTIONS --------------

def get_image_paths(base_path, folder):
    os.chdir(base_path+folder)
    image_names=glob.glob("*.*")
    image_names=[folder + img for img in image_names]
    os.chdir(base_path)
    return image_names

def preprocess_list_of_images(list_of_paths):
  images = [cv2.imread(file) for file in list_of_paths]
  images = [cv2.cvtColor(image, cv2.COLOR_BGR2RGB) for image in images]
  return [image.reshape((image.shape[0] * image.shape[1], 3)) for image in images]

def find_dominant_colours(path, folder, n_clstrs): 
  list_of_paths=get_image_paths(path, folder+"/")
  images = preprocess_list_of_images(list_of_paths)
  dom=[]
  for i in range(0,len(images)):
      cltr = KMeans(n_clusters = n_clstrs)
      dan = [list_of_paths[i]]
      rgb = np.rint(cltr.fit(images[i]).cluster_centers_).astype(int).tolist()
      dan.extend(rgb)
      dom.append(dan)
  clms=['color'+str(i) for i in range(0,n_clstrs)]
  with open(folder + "_metadata/colour_rgb.csv", "w", newline="") as f:
            header = ['ImgName']
            header.extend(clms)
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(dom)

# -------------------------------------------------------

