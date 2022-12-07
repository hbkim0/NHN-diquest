
import torch
from torch.nn import Module, Identity, CosineEmbeddingLoss
from torchvision.models import resnet18, resnet34, resnet50, resnet101, resnet152

from dataset import ContrastiveDataset

from albumentations import Compose, Normalize, Resize
from albumentations.pytorch import ToTensorV2

resnet_layers = {
    18: resnet18,
    34: resnet34,
    50: resnet50,
    101: resnet101,
    152: resnet152,
}

class ResNet(Module):

    def __init__(
        self,
        num_layers: int = 18,
        pretrained: bool = False,
    ):
        super(ResNet, self).__init__()
        self.resnet = resnet_layers[num_layers](pretrained = pretrained)
        self.resnet.fc = Identity()
        
    def forward(self, x):
        output = self.resnet(x)
        return output

# for test
if __name__=="__main__":

    dataset = ContrastiveDataset("data/train.json", Compose([Resize(224, 224), Normalize(), ToTensorV2()]))
    model = ResNet(num_layers=50, pretrained=True)

    sample = dataset[0]

    output_0 = model(sample["sample_0"].unsqueeze(0))
    output_1 = model(sample["sample_1"].unsqueeze(0))
    print(output_0.shape)

    criterion = CosineEmbeddingLoss()

    loss = criterion(output_0, output_1, torch.tensor(sample["labels"]).unsqueeze(0))
    print("different sample's loss: {}".format(loss.item()))

    sample = dataset[11]

    output_0 = model(sample["sample_0"].unsqueeze(0))
    output_1 = model(sample["sample_1"].unsqueeze(0))

    criterion = CosineEmbeddingLoss()

    loss = criterion(output_0, output_1, torch.tensor(sample["labels"]).unsqueeze(0))
    print("same sample's loss: {}".format(loss.item()))

    