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

def find_dominant_colours(list_of_paths, n_clstrs): 
  images = preprocess_list_of_images(list_of_paths)
  dom=[]
  for i in range(0,len(images)):
      cltr = KMeans(n_clusters = n_clstrs)
      dom.append((list_of_paths[i], np.rint(cltr.fit(images[i]).cluster_centers_).astype(int)))
  return dom

def get_name_of_nearest_colour(dictionary, rgb):
    names = []
    rgb_values = []
    for color_name, color_rgb in dictionary.items():
        names.append(color_name)
        rgb_values.append(ast.literal_eval(color_rgb))
  
    kdt_db = KDTree(rgb_values)
    distance, index = kdt_db.query(tuple(rgb))
    return names[index]

def get_dict(filename) :       
    with open(filename, mode='r') as infile:
        reader = csv.reader(infile)
        return {rows[0]:rows[1] for rows in reader}

def get_colour_names_of_all_images(path, folder, dict_file, n_clstrs):
    dictionary=get_dict(dict_file)
    list_names=get_image_paths(path, folder)
    aa=find_dominant_colours(list_names, n_clstrs)
    for rgb in aa:
        cl=[]
        print(rgb[0])
        for l in range(1,n_clstrs):
            cl.append(get_name_of_nearest_colour(dictionary, rgb[1][l]))
        print(set(cl))


# -------------------------------------------------------



