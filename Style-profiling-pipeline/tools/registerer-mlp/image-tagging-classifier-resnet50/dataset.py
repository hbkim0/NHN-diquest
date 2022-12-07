from pathlib import Path

import json
import yaml
import numpy as np
from PIL import Image

from torchvision import transforms
from torch.utils.data import Dataset


IMG_SIZE = [224, 224]


class ImageTaggingDataset(Dataset):
    def __init__(self, dir, purpose, normalize=True):
        self.dir = dir
        if normalize:
            self.transforms = transforms.Compose([
                transforms.Resize(IMG_SIZE),
                transforms.ToTensor(),
                transforms.Normalize(
                    [0.485, 0.456, 0.406], 
                    [0.229, 0.224, 0.225]
                )
            ])
        else:
            self.transforms = transforms.Compose([
                transforms.Resize(IMG_SIZE),
                transforms.ToTensor()
                ])

        with open(Path(dir, 'dataset.yaml'), 'r') as f:
            info = yaml.load(f, Loader=yaml.FullLoader)

        self.nc = info['nc']
        self.path = Path(info['path'], info[purpose])

        self.image_name_list = []
        self.labels = []
        for file_path in Path(self.path, 'images').iterdir():
            json_name = file_path.with_suffix('.json').name
            self.image_name_list.append(file_path)
            
            with open(Path(self.path, 'labels', json_name), 'r') as f:
                tmp = json.load(f)

            label = [0, ] * self.nc
            for i in tmp['labels']:
                label[i] += 1
            self.labels.append(label)
    
    def get_nc(self):
        return self.nc

    def __len__(self) -> int:
        return len(self.labels)

    def __getitem__(self, index: int):
        image_name = self.image_name_list[index]
        image = Image.open(image_name).convert('RGB')
        target = np.array(self.labels[index]).astype(np.float32)

        if self.transforms is not None:
            image = self.transforms(image)
        
        return image, target
