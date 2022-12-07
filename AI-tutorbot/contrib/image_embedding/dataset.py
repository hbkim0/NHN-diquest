
import json
import os
import cv2
import random

from torch.utils.data import Dataset

class SingleSampleEmbeddingDataset(Dataset):
    
    def __init__(
        self,
        image_root: str = None,
        transform = None,
    ):
        self.data = [image_root + image for image in sorted(os.listdir(image_root))]
        self.transform = transform

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        sample = self.data[index]

        sample = cv2.imread(sample)
        sample = self.transform(image = sample)["image"]

        return {"sample": sample}

class ContrastiveDataset(Dataset):

    def __init__(
        self,
        data_path: str = None,
        transform = None,
        proper_mixture: bool = False,
    ):
        data = json.load(open(data_path, 'r'))
        self.data = []

        if proper_mixture:
            match_ratio = 0

            for d in data:
                if d["sample_0"] == d["sample_1"]: match_ratio += 1
            
            match_ratio /= len(data)
            match_ratio = round(int(1 / match_ratio))

            for d in data:
                if d["sample_0"] == d["sample_1"]: self.data.extend([d] * match_ratio)
                else: self.data.append(d)

            random.shuffle(self.data)
        
        else:
            self.data = data

        self.transform = transform

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        sample = self.data[index]

        labels = -1

        if sample["sample_0"] == sample["sample_1"]:
            labels = 1

        sample_0 = cv2.imread(sample["sample_0"])
        sample_1 = cv2.imread(sample["sample_1"])

        sample_0 = self.transform(image = sample_0)["image"]
        sample_1 = self.transform(image = sample_1)["image"]

        return {"sample_0": sample_0, "sample_1": sample_1, "labels": labels}

class TripletDataset(Dataset):

    def __init__(
        self,
        data_path: str = None,
        transform = None,
    ):
        data = json.load(open(data_path, 'r'))
        
        self.data = []
        for d in data:
            if d["sample_0"] != d["sample_1"]:
                self.data.append(d)

        self.transform = transform

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        sample = self.data[index]

        anchor = cv2.imread(sample["sample_0"])
        positive = cv2.imread(sample["sample_0"])
        negative = cv2.imread(sample["sample_1"])

        anchor = self.transform(image = anchor)["image"]
        positive = self.transform(image = positive)["image"]
        negative = self.transform(image = negative)["image"]

        return {"anchor": anchor, "positive": positive, "negative": negative}