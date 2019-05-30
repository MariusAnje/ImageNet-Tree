import torch
import torchvision
from torchvision import transforms
import sklearn
from sklearn import tree
from tqdm import tqdm_notebook
import numpy as np

traindir = '/home/yanzy/data/train'
valdir = '/home/yanzy/data/val'
normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225])

val_loader = torch.utils.data.DataLoader(
    torchvision.datasets.ImageFolder(valdir, transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        normalize,
    ])),
    batch_size=1, shuffle=False,
    num_workers=16, pin_memory=True)
#val_loader = torch.utils.data.DataLoader(val_dataset, batch_size=64,
#                                         shuffle=False, num_workers = 16, pin_memory=False)

train_dataset =  torchvision.datasets.ImageFolder(
    traindir,
    transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        normalize,
]))
train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=16,
                                         shuffle=False, num_workers = 4, pin_memory=False)

model = torchvision.models.vgg16(pretrained= True)

model.eval()
features = []
labels = []
i = 0
with torch.no_grad():
    for data in tqdm_notebook(train_loader):
        image, label = data
        Y = model.features(image).view(-1,25088)
        features += Y.numpy().tolist()
        labels += label.numpy().tolist()
        i += 1
        
np.save('features',features)
np.save('labels', labels)