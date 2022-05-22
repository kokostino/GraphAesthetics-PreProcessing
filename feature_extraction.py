import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision
from torchvision import datasets, transforms, models
from torch.autograd import Variable
from PIL import Image
import os

model = models.resnet18(pretrained=True)


def feature_vector_resnet18(img_path):
  img=Image.open(img_path)
  scaler = transforms.Resize((224))
  normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225])
  to_tensor = transforms.ToTensor()

  t_img=Variable(normalize(to_tensor(scaler(img).convert('RGB'))).unsqueeze(0))

  new_model = nn.Sequential(*list(model.children())[:-1])

  return new_model(t_img).detach().numpy().reshape(-1)

def feature_vectors_of_folder(folder):
  cl=[]
  for image in os.listdir(folder):
    cl.append([image, feature_vector_resnet18(folder + "/" + image)])
  print(cl)
  
