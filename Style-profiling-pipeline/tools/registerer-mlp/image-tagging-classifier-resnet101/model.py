from torch import nn
from torchvision.models import resnet101


class ImageTaggingModel(nn.Module):
    def __init__(self, nc) -> None:
        super().__init__()
        self.resnet = resnet101(pretrained=True)
        self.classifier = nn.Linear(1000, nc)

    def forward(self, x):
        x = self.resnet(x)
        x = self.classifier(x)

        return x
