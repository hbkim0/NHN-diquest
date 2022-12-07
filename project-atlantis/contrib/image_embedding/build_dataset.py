
from argparse import ArgumentParser
import json
import os
import random

def parse_args():

    parser = ArgumentParser()

    parser.add_argument("-i", "--input_path", default="images/")

    return parser.parse_args()

def build_dataset(args):

    input_path = args.input_path

    if input_path.endswith('/') is False: input_path += '/'
    images = [input_path + image for image in os.listdir(input_path)]

    images.sort()

    result = []

    for image_0 in images:
        for image_1 in images:
            result.append({"sample_0": image_0, "sample_1": image_1})

    random.shuffle(result)

    train_len = int(len(result) * 0.9)

    return result[:train_len], result[train_len:]

if __name__=="__main__":

    args = parse_args()
    train_set, eval_set = build_dataset(args)

    with open("data/train.json", 'w') as f:
        json.dump(train_set, f, ensure_ascii=False, indent='\t')
        print("{} samples saved in {}".format(len(train_set), "data/train.json"))

    with open("data/eval.json", 'w') as f:
        json.dump(eval_set, f, ensure_ascii=False, indent='\t')
        print("{} samples saved in {}".format(len(eval_set), "data/eval.json"))