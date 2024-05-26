from torch.nn import Module, Conv2d, Linear, MaxPool2d, AdaptiveAvgPool1d
from torch.nn.functional import relu, dropout
from imageLoader import *

class Network(Module):
    def __init__(self) -> None:
        super(Network, self).__init__()
        # input channel RGB 3 channel, kernel size
        # 1. Convolutional Layer takes image as input
        self.conv_1 = Conv2d(in_channels=3, out_channels=64, kernel_size=5)
        self.conv_2 = Conv2d(in_channels=64, out_channels=128, kernel_size=3)
        self.conv_3 = Conv2d(in_channels=128, out_channels=256, kernel_size=5)

        self.maxPooling = MaxPool2d(kernel_size=4)
        # 256: input feature of Fully connected layer
        # so that it automatically calculate the difference between convolutional and fully connected layer
        self.adPooling = AdaptiveAvgPool1d(256)

        # 2. Fully connected Layer takes pixel as input
        self.fc1 = Linear(in_features=256, out_features=128)
        self.fc2 = Linear(in_features=128, out_features=64)
        # out_feature: binary(cat or dog)
        self.out = Linear(in_features=64, out_features=2)

    # x: input
    def forward(self, x):
        x = self.conv_1(x)
        # add additional layers in between: maxPool
        x = self.maxPooling(x)
        x = relu(x)

        x = self.conv_2(x)
        x = self.maxPooling(x)
        x = relu(x)

        x = self.conv_3(x)
        x = self.maxPooling(x)
        x = relu(x)

        # adaptive pooling layer betweeen convolutional and fully connected layer!
        # stretch the output of the convolution layer into 1 dimensional data
        # also dropout layer in between to help improve the performance of the layer
        x = dropout(x)
        x = x.view(1, x.size()[0], -1)
        x = self.adPooling(x).squeeze()

        x = self.fc1(x)
        x = relu(x)

        x = self.fc2(x)
        x = relu(x)

        return relu(self.out(x))


imageLoader = ImageLoader(trainData, transform)

# load data
dataLoader = DataLoader(imageLoader, batch_size=10, shuffle=True)

data = iter(dataLoader)

images = next(data)

network = Network()
out = network(images[0])

# list of [probability of being a cat, prob(dog)]
# tensor([[0.0000, 0.0761],
#         [0.0000, 0.0601],
#         [0.0000, 0.0704],
#         [0.0000, 0.0754],
#         [0.0000, 0.0527],
#         [0.0000, 0.0793],
#         [0.0000, 0.0648],
#         [0.0000, 0.0527],
#         [0.0000, 0.0556],
#         [0.0000, 0.0558]], grad_fn=<ReluBackward0>)
# after training they would be close to 0 or 1
print(out)
print(out.size()) # torch.Size([10, 2])


