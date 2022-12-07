
import json
import os

from argparse import ArgumentParser
from tqdm import tqdm

from albumentations.pytorch import ToTensorV2
from albumentations import (
    Compose,
    Resize,
    RandomCrop,
    GridDistortion,
    ShiftScaleRotate,
    RandomBrightnessContrast,
    ImageCompression,
    JpegCompression,
    Normalize
)

from model import ResNet
from dataset import ContrastiveDataset, SingleSampleEmbeddingDataset, TripletDataset

import torch
from torch.nn import CosineEmbeddingLoss, CosineSimilarity, TripletMarginLoss
from torch.optim import AdamW
from torch.optim.lr_scheduler import LambdaLR
from torch.utils.data import DataLoader

def parse_args():

    parser = ArgumentParser()

    parser.add_argument("-t", "--task", choices=["train", "eval"])
    parser.add_argument("-d", "--data_root", default="data/")
    parser.add_argument("-f", "--train_form", choices=["contrastive", "triplet"])
    parser.add_argument("-m", "--model_path")
    parser.add_argument("-l", "--num_layers", default=18, type=int)
    parser.add_argument("-b", "--batch_size", default=16, type=int)
    parser.add_argument("-e", "--early_stop_patience", default=3, type=int)
    parser.add_argument("-s", "--save_root", default="trained_model/")
    
    return parser.parse_args()

def get_dataloader(
    data_path: str = None,
    batch_size: int = None,
    is_triplet: bool = False,
    transform = None,
    proper_mixture: bool = False,
):

    if transform is None:
        transform = Compose([
            Resize(256, 256),
            RandomCrop(224, 224),
            GridDistortion(),
            ShiftScaleRotate(),
            RandomBrightnessContrast(),
            ImageCompression(),
            JpegCompression(),
            Normalize(),
            ToTensorV2(),
        ])

    if is_triplet:
        dataset = TripletDataset(
            data_path = data_path,
            transform = transform,
            proper_mixture = proper_mixture
        )
    else:
        dataset = ContrastiveDataset(
            data_path = data_path,
            transform = transform,
            proper_mixture = proper_mixture
        )

    return DataLoader(
        dataset = dataset,
        batch_size = batch_size,
        shuffle = False,
    )

def eval(args):

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    model = ResNet()
    model.load_state_dict(torch.load(args.model_path))
    model.to(device)

    data_root = args.data_root if args.data_root.endswith('/') else args.data_root + '/'

    transform = Compose([
        Resize(224, 224),
        # RandomCrop(224, 224),
        # GridDistortion(),
        # ShiftScaleRotate(),
        # RandomBrightnessContrast(),
        # ImageCompression(),
        # JpegCompression(),
        Normalize(),
        ToTensorV2(),
    ])

    eval_set = SingleSampleEmbeddingDataset(
        image_root = data_root,
        transform = transform,
    )

    eval_loader = DataLoader(
        eval_set,
        batch_size = args.batch_size,
        shuffle = False,
    )

    result = []
    model.eval()

    for batch_index, batch in enumerate(tqdm(eval_loader)):

        sample = batch["sample"].to(device)

        with torch.no_grad():
            output = model(sample)

        for i, dense in enumerate(output):
            index = (batch_index * args.batch_size) + i + 1
            result.append({"index": index, "dense": dense.tolist()})

    with open("2-non_augmented.json", 'w') as f:
        json.dump(result, f, ensure_ascii=False, indent="\t")

def train(args):

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    model = ResNet(pretrained = True)
    model.to(device)

    data_root = args.data_root if args.data_root.endswith('/') else args.data_root + '/'
    save_root = args.save_root if args.save_root.endswith('/') else args.save_root + '/'

    train_loader = get_dataloader(
        data_path = data_root + 'train.json',
        batch_size = args.batch_size,
        is_triplet = args.train_form == "triplet",
        proper_mixture = True,
    )

    eval_transform = Compose([
        Resize(256, 256),
        RandomCrop(224, 224),
        Normalize(),
        ToTensorV2(),
    ])

    eval_loader = get_dataloader(
        data_path = data_root + "eval.json",
        batch_size = args.batch_size,
        is_triplet = args.train_form == "triplet",
        # transform = eval_transform,
        proper_mixture = True,
    )

    optimizer = AdamW(model.parameters(), lr = 5e-5)

    if args.train_form == "contrastive":
        criterion = CosineEmbeddingLoss()
    else:
        criterion = TripletMarginLoss()

    scheduler = LambdaLR(optimizer=optimizer, lr_lambda=lambda epoch: 0.95 ** epoch)

    best_loss = 1e+5
    patience = 0

    for epoch in range(10000):

        model.train()
        train_loss = 0.

        for batch_index, batch in enumerate(tqdm(train_loader)):

            optimizer.zero_grad()

            if args.train_form == "contrastive":
                sample_0 = batch["sample_0"].to(device)
                sample_1 = batch["sample_1"].to(device)
                labels = batch["labels"].to(device)

                output_0 = model(sample_0)
                output_1 = model(sample_1)

                loss = criterion(output_0, output_1, labels)

            elif "anchor" in batch:
                anchor = batch["anchor"].to(device)
                positive = batch["positive"].to(device)
                negative = batch["negative"].to(device)

                output_anchor = model(anchor)
                output_positive = model(positive)
                output_negative = model(negative)

                loss = criterion(output_anchor, output_positive, output_negative)

            train_loss += loss.item()

            print("epoch: {}\tloss: {}".format(
                round(epoch + (batch_index / len(train_loader)), 2),
                round(loss.item(), 4)
            ))

            loss.backward()
            optimizer.step()
        
        scheduler.step()

        train_loss = round(train_loss / len(train_loader), 4)
        print("{} - train_losses: {}".format(epoch, train_loss))

        model.eval()
        eval_loss = 0.

        for batch_index, batch in enumerate(eval_loader):

            if args.train_form == "contrastive":

                sample_0 = batch["sample_0"].to(device)
                sample_1 = batch["sample_1"].to(device)
                labels = batch["labels"].to(device)

                with torch.no_grad():
                    output_0 = model(sample_0)
                    output_1 = model(sample_1)

                loss = criterion(output_0, output_1, labels)

            else:

                anchor = batch["anchor"].to(device)
                positive = batch["positive"].to(device)
                negative = batch["negative"].to(device)

                with torch.no_grad():
                    output_anchor = model(anchor)
                    output_positive = model(positive)
                    output_negative = model(negative)

                loss = criterion(output_anchor, output_positive, output_negative)

            eval_loss += loss.item()

        eval_loss = round(eval_loss / len(eval_loader), 4)
        print("{} - eval_losses: {}".format(epoch, eval_loss))

        if eval_loss < best_loss:
            best_loss = eval_loss
            patience = 0

            if len(os.listdir(save_root)) != 0:
                os.remove(save_root + os.listdir(save_root)[0])

            torch.save(model.state_dict(), save_root + '{}.pt'.format(epoch))
        else:
            patience += 1

        if patience == args.early_stop_patience:
            print("patience is over.")
            break

if __name__=="__main__":

    args = parse_args()

    if args.task == "train":
        train(args)
    elif args.task == "eval":
        eval(args)