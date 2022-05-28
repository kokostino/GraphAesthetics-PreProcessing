import torch.nn as nn
import torch.nn.functional as F
from torchvision import transforms, models
from torch.autograd import Variable
from PIL import Image
import os
import csv

## model = models.resnet18(pretrained=True)

def feature_vector_resnet18(model, img_path):
  img=Image.open(img_path)
  scaler = transforms.Resize((224))
  normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225])
  to_tensor = transforms.ToTensor()

  t_img=Variable(normalize(to_tensor(scaler(img).convert('RGB'))).unsqueeze(0))
  
  new_model = nn.Sequential(*list(model.children())[:-1])
  
  fv = [img_path.rsplit('/')[-1]]
  fv.extend(list(new_model(t_img).detach().numpy().reshape(-1)))
  return fv

def feature_vectors_of_folder(folder):
  
  model = models.resnet18(pretrained=True)

    
  cl=[]
  for image in os.listdir(folder):
    cl.append(feature_vector_resnet18(model, folder + "/" + image))  
    
  with open(folder + "_metadata/feature_vectors.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(cl)

