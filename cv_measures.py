# ------- IMPORT --------------

from sklearn.cluster import KMeans
from numpy.linalg import norm
import numpy as np
import cv2
import glob
import os
import csv

    
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

def brightness(img):
    if len(img.shape) == 3:
        return np.average(norm(img, axis=2)) / np.sqrt(3)
    else:
        return np.average(img)

def contrast(image):
    img = cv2.imread(image)
    lab = cv2.cvtColor(img,cv2.COLOR_BGR2LAB)
    L,A,B=cv2.split(lab)

    # compute minimum and maximum in 5x5 region using erode and dilate
    kernel = np.ones((5,5),np.uint8)
    min = cv2.erode(L,kernel,iterations = 1)
    max = cv2.dilate(L,kernel,iterations = 1)

    # convert min and max to floats
    min = min.astype(np.float64) 
    max = max.astype(np.float64) 
    epsilon=0.00000000001
    # compute local contrast
    contrast = (max-min)/(max+min+epsilon)
    
    # get average across whole image
    average_contrast = 100*np.mean(contrast)
    return average_contrast
    
def computer_vision_measures(path, folder): 
    list_of_paths=get_image_paths(path, folder+"/")
    images = preprocess_list_of_images(list_of_paths)
    dom=[]
    for i in range(0,len(images)):
        dan = [list_of_paths[i].rsplit('/')[-1]]
        
        # KMeans: THE dominant colour
        cltr = KMeans(n_clusters = 1)
        rgb = np.rint(cltr.fit(images[i]).cluster_centers_).astype(int)[0].tolist()
        dan.extend(rgb)
        # brightness
        br=[round(brightness(images[i]))]
        dan.extend(br)
        # contrast
        ctr = [round(contrast(list_of_paths[i]))]
        dan.extend(ctr)
        
        dom.append(dan)
    
    with open(folder + "_metadata/cv.csv", "w", newline="") as f:
            header = ['ImgName','R','G','B','Brightness','Contrast']
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(dom)

# -------------------------------------------------------

