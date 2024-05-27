# EP2: Data preprocessing

"""
1. Remove grayscale images (a single channel image)
2. Make the image square shaped -> (3,200,200)
3. Converts image matrix -> tensor: (torch,Size([3, 200, 200]), 0)
    ; 3 channels with width and height of 200 and label=0
4. DataLoader pytorch class: take list of images and squeeze into a matrix 
    (torch.Size([9,3,200,200]), tensor([1,0,1,0,1,1,1,1,0]))
"""
from torchvision.datasets import ImageFolder
from sklearn.model_selection import train_test_split
from torch.utils.data import Dataset, DataLoader
from PIL import Image
from torchvision import transforms

transform = transforms.Compose([
    # resize to 200,200
    transforms.Resize((200,200)),
    # transform into Tensor data type
    transforms.ToTensor(),
    # normalize https://pytorch.org/vision/main/generated/torchvision.transforms.Normalize.html
    # transforms.Normalize([.5, .5, .5], [.5, .5, .5])
    # Mean of .5 and Standard Deviation of .5 for 3 RGB channels
    transforms.Normalize([.5] * 3, [.5] * 3)
])

dataset = ImageFolder("backend/worker/pytorch/data")
# labels cat:0, dog:1
# print(dataset.targets)
# classes ['cats', 'dogs']
# print(dataset.classes)

# split data into test/train dataset
trainData, testData, trainLabel, testLabel = train_test_split(dataset.imgs, dataset.targets, test_size=0.2, random_state=0)
# check paths to images
# print(trainData)
# print(testData)


class ImageLoader(Dataset):
    def __init__(self, dataset, transform=None):
        self.dataset = self.checkChannel(dataset)
        self.transform = transform

    # 1. Remove grayscale images (a single channel image)
    def checkChannel(self, dataset):
        datasetRGB = []
        for index in range(len(dataset)):
            # print(Image.open(dataset[index][0]).getbands())
            if Image.open(dataset[index][0]).getbands() == ('R', 'G', 'B'):
                datasetRGB.append(dataset[index])

        return datasetRGB

    # 2. Make the image square shaped -> (3,200,200)
    def getResizedImage(self, item):
        image = Image.open(self.dataset[item][0])
        # get bounding box of the image
        _, _, width, height = image.getbbox()
        factor = (0, 0, width, width) if width > height else (0, 0, height, height)
        return image.crop(factor)

    # 3. Converts image -> Tensor: (torch,Size([3, 200, 200]), 0)
    #    ; 3 channels with width and height of 200 and label=0

    # returns PIL image object and label
    def __getitem__(self, item):
        image = self.getResizedImage(item)
        if transform is not None:
            return self.transform(image), self.dataset[item][1]

        return image, self.dataset[item][1]

    def __len__(self):
        return len(self.dataset)



imageLoader = ImageLoader(trainData, transform)
# print(imageLoader[0][0])
# print(imageLoader[0][0].size()) # torch.Size([3, 200, 200])

# load data
dataLoader = DataLoader(imageLoader, batch_size=10, shuffle=True)

data = iter(dataLoader)

# d = next(data)
# # size of weight
# print(d[0])
# # batch size = 10
# print(d[0].size()) # torch.Size([10, 3, 200, 200])
