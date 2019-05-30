import torch
from torch import nn


class VAE(nn.Module):
    def __init__(self):
        super(VAE, self).__init__()
        hiddenSize = 384 * 2 * 2
        self.conv1 = nn.Conv2d(3, 64, 5, padding = 2)
        self.conv2 = nn.Conv2d(64, 192, 5, padding = 2)
        self.conv3 = nn.Conv2d(192, 384, 5, padding = 2)
        self.conv4 = nn.Conv2d(384, 192, 3, padding = 1)
        self.fc11 = nn.Linear(384 * 4 * 4, hiddenSize)
        self.fc12 = nn.Linear(384 * 4 * 4, hiddenSize)
        self.fc2  = nn.Linear(hiddenSize, 384 * 4 * 4)
        self.deconv4 = nn.ConvTranspose2d(192, 384, 3, padding = 0, stride = 2)
        self.deconv3 = nn.ConvTranspose2d(384, 192, 5, padding = 1, stride = 2)
        self.deconv2 = nn.ConvTranspose2d(192, 64, 5, padding = 1, stride = 2)
        self.deconv1 = nn.ConvTranspose2d(64, 3, 5, padding = 1, stride = 2)
        self.pool = nn.MaxPool2d(2, stride=2)
        self.relu = nn.LeakyReLU()
        self.sigmoid = nn.Sigmoid()
    
    def encode(self, x):
        x1 = self.pool(self.relu(self.conv1(x)))
        x2 = self.pool(self.relu(self.conv2(x1)))
        x3 = self.pool(self.relu(self.conv3(x2)))
        #x4 = self.pool(self.relu(self.conv4(x3)))
        x = x3.view(-1, 384 * 4 * 4)
        return self.fc11(x), self.fc12(x)
    
    def reparameterize(self, mu, logvar):
        if self.training:
            std = logvar.mul(0.5).exp_()
            eps = torch.randn_like(std)
            return eps.mul(std).add_(mu)
        else:
            return mu
    
    def decode(self, z):
        z = self.relu(self.fc2(z))
        z = self.relu(z.view(-1, 384, 4, 4))
        #z = self.relu(self.deconv4(z))[:,:,1:,1:]
        z = self.relu(self.deconv3(z))[:,:,1:,1:]
        z = self.relu(self.deconv2(z))[:,:,1:,1:]
        #return self.sigmoid(self.deconv1(z))[:,:,1:,1:]
        return self.deconv1(z)[:,:,1:,1:]
    
    def forward(self, x):
        mu, logvar = self.encode(x)
        z = self.reparameterize(mu, logvar)
        return self.relu(self.decode(z)), mu, logvar