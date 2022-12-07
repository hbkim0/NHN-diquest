# 테스트 목적의 코드. docker에 포함할 형태로 작성되지 않음.
import argparse
import os

import yaml
import json
import torch

from PIL import Image
from torchvision import transforms


def main(opt):
    model = torch.jit.load(opt.model)
    model = model.to(opt.device)
    input = preprocess(opt.image, opt.device)
    output = model(input)
    result = postprocess(output, opt.threshold, opt.data, opt.label)

    if opt.label is not None:
        print('ground truth labels')
        for i in result['labels']:
            print(i.split('::')[1], end=' ')
        print()
    print('predicted labels')
    for i in result['predicted']:
        print(i.split('::')[1], end=' ')
    print()


def preprocess(image_path, device):
    T = transforms.Compose([
        transforms.Resize([224, 224]), 
        transforms.ToTensor(),
        transforms.Normalize(
            [0.485, 0.456, 0.406], 
            [0.229, 0.224, 0.225]
        )
    ])
    result = Image.open(image_path).convert('RGB')
    result = T(result)
    result = result.unsqueeze(0)
    result = result.to(device)

    return result


def postprocess(output, threshold, dataset_path=None, label_path=None):
    output = output > threshold
    output = output.squeeze()
    output = output.int().tolist()

    if dataset_path:
        with open(os.path.join(dataset_path, 'dataset.yaml'), 'r') as f:
            yaml_file = yaml.load(f, Loader=yaml.FullLoader)
        predicted = []
        for i, v in enumerate(output):
            if v:
                predicted.append(yaml_file['names'][i])

        result = {}
        result['predicted'] = sorted(predicted)

        if label_path:
            with open(label_path, 'r') as f:
                json_file = json.load(f)
            labels = []
            for i in json_file['labels']:
                labels.append(yaml_file['names'][i])
            result['labels'] = sorted(labels)
        
        return result
    else:
        return output


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', type=str, default='best.pt', help='model.pt path')
    parser.add_argument('--image', type=str, default='', help='image.jpg path')
    parser.add_argument('--label', default=None, help='label.json path if exist')
    parser.add_argument('--data', type=str, default='dataset', help='dataset.yaml path')
    parser.add_argument('--device', default='cpu', help='cpu or cuda')
    parser.add_argument('--top-n', type=int, default=0)
    parser.add_argument('--threshold', type=float, default=0.0)

    opt = parser.parse_args()
    return opt


if __name__ == "__main__":
    opt = parse_opt()
    main(opt)