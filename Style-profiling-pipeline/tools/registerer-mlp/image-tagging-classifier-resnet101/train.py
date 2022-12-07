from cProfile import run
import os
import argparse

import mlflow
import mlflow.pytorch
import torch
import torchvision

from torch import nn, optim
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter

from dataset import ImageTaggingDataset
from model import ImageTaggingModel


def main(opt):
    if not os.path.isfile(os.path.join(opt.data, 'dataset.yaml')):
        print('dataset.yaml not exist')
        return

    # Mlflow setting
    artifacts_path = 'model'
    mlflow.set_tracking_uri('http://133.186.171.5:5002')
    
    with mlflow.start_run() as run:    
        print('---loader')
        training_dataset = ImageTaggingDataset(opt.data, 'train')
        validation_dataset = ImageTaggingDataset(opt.data, 'val')
        nc = training_dataset.get_nc()

        training_loader = DataLoader(training_dataset, shuffle=True, batch_size=opt.batch_size, num_workers=1)
        validation_loader = DataLoader(validation_dataset, batch_size=1, num_workers=1)

        print('---model')
        device = torch.device(opt.device)
        model = ImageTaggingModel(nc).to(device)

        optimizer = optim.Adam(model.parameters(), lr=1e-3)
        criterion = nn.MultiLabelSoftMarginLoss()
        
        writer = SummaryWriter(opt.output_path)

        print('---start training')

        for epoch in range(opt.epochs):
            model.train()
            total_train_loss = 0.0
            total_train_acc = 0.0
            for i, (images, targets) in enumerate(training_loader):
                optimizer.zero_grad()

                images = images.to(device)
                targets = targets.to(device)

                outputs = model(images)
                loss = criterion(outputs, targets)

                loss.backward()
                total_train_loss += loss.item()
                optimizer.step()
                    
                outputs = outputs > opt.threshold
                step_acc = (outputs == targets).float().mean()
                total_train_acc += step_acc
                
                writer.add_scalar('Training/loss per step', loss.item(), epoch * len(training_loader) + i)
                writer.add_scalar('Training/accuracy per step', step_acc, epoch * len(training_loader) + i)

                train_loss = total_train_loss / (i+1)
                train_acc = total_train_acc / (i+1)

            model.eval()
            with torch.no_grad():
                total_val_loss = 0.0
                total_val_acc = 0.0
                for i, (images, targets) in enumerate(validation_loader):
                    images = images.to(device)
                    targets = targets.to(device)

                    outputs = model(images)
                    loss = criterion(outputs, targets)
                    total_val_loss += loss.item()

                    outputs = outputs > opt.threshold
                    total_val_acc += (outputs == targets).float().mean()

                val_loss = total_val_loss / (i+1)
                val_acc = total_val_acc / (i+1)

                writer.add_scalar('Validation/loss per epoch', val_loss, epoch)
                writer.add_scalar('Validation/accuracy per epoch', val_acc, epoch)

            print(f'epoch: {epoch+1}')
            print(f'train loss: {train_loss:.5f} | train acc: {train_acc:.5f}')
            print(f'  val loss: {val_loss:.5f} |   val acc: {val_acc:.5f}')
            print()

        # mlflow log params
        mlflow.log_param('epoch', opt.epochs)
        mlflow.log_param('batch_size', opt.batch_size)
        # mlflow log metrics
        # mlflow.log_metric('Train accuracy', train_acc)
        mlflow.log_metric('Val accuracy', val_acc)

        # mlflow log model
        mlflow.pytorch.log_model(model, artifact_path = artifacts_path)

    model_uri_ = f"runs:/{run.info.run_id}/{artifacts_path}"
    mlflow.register_model(model_uri=model_uri_, name='ImageClassifier')

    print('---tensorboard summary')
    tb_train_dataset = ImageTaggingDataset(opt.data, 'train', normalize=False)
    tb_val_dataset = ImageTaggingDataset(opt.data, 'val', normalize=False)
    tb_train_loader = DataLoader(tb_train_dataset, shuffle=True, batch_size=opt.batch_size, num_workers=1)
    tb_val_loader = DataLoader(tb_val_dataset, shuffle=True, batch_size=opt.batch_size, num_workers=1)

    dataiter = iter(tb_train_loader)
    images, _ = dataiter.next()
    images = images.to(device)
    img_grid = torchvision.utils.make_grid(images)
    writer.add_image("resized_training_images", img_grid)

    dataiter = iter(tb_val_loader)
    images, _ = dataiter.next()
    images = images.to(device)
    img_grid = torchvision.utils.make_grid(images)
    writer.add_image("resized_validation_images", img_grid)

    writer.add_graph(model, images)
    writer.close()    
    
    print('---save result')
    os.makedirs(opt.output_path, exist_ok=True)
    jit_model = torch.jit.script(model)
    torch.jit.save(jit_model, os.path.join(opt.output_path, 'last.pt'))


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', type=str, default='dataset', help='dataset.yaml path')
    parser.add_argument('--epochs', type=int, default=2)
    parser.add_argument('--batch-size', type=int, default=16)
    parser.add_argument('--device', default='cpu', help='cpu or cuda')
    # parser.add_argument('--project', default='exp_results')
    # parser.add_argument('--name', default='results')
    parser.add_argument('--output-path', default='exp_results/results')
    # parser.add_argument('--top-n', type=int, default=0)
    parser.add_argument('--threshold', type=float, default=0.0, help='set decision boundary for output score(default: 0.0)')

    opt = parser.parse_args()
    return opt


if __name__ == "__main__":
    opt = parse_opt()
    main(opt)