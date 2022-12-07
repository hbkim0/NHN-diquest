# coding=utf-8
# Copyright 2018 The Google AI Language Team Authors and The HuggingFace Inc. team.
# Copyright (c) 2018, NVIDIA CORPORATION.  All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
""" Fine-tuning the library models for named entity recognition on CoNLL-2003. """

from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import json

import logging
import os
import sys
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

import numpy as np
from seqeval.metrics import f1_score, precision_score, recall_score
from torch import nn

from transformers import (
    AutoConfig,
    AutoModelForTokenClassification,
    AutoTokenizer,
    EvalPrediction,
    HfArgumentParser,
    Trainer,
    TrainingArguments,
    set_seed,
)

from utils_fashion import NerDataset, Split, get_labels, FashionDataset

from soynlp.hangle import levenshtein

from preprocessing.preprocess import read_category

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app)

os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"]="0"

@dataclass
class ModelArguments:
    """
    Arguments pertaining to which model/config/tokenizer we are going to fine-tune from.
    """

    model_name_or_path: str = field(
        metadata={"help": "Path to pretrained model or model identifier from huggingface.co/models"}
    )
    config_name: Optional[str] = field(
        default=None, metadata={"help": "Pretrained config name or path if not the same as model_name"}
    )
    tokenizer_name: Optional[str] = field(
        default=None, metadata={"help": "Pretrained tokenizer name or path if not the same as model_name"}
    )
    use_fast: bool = field(default=False, metadata={"help": "Set this flag to use fast tokenization."})
    # If you want to tweak more attributes on your tokenizer, you should do it in a distinct script,
    # or just modify its tokenizer_config.json.
    cache_dir: Optional[str] = field(
        default=None, metadata={"help": "Where do you want to store the pretrained models downloaded from s3"}
    )


@dataclass
class DataTrainingArguments:
    """
    Arguments pertaining to what data we are going to input our model for training and eval.
    """

    data_dir: str = field(
        metadata={"help": "The input data dir. Should contain the .txt files for a CoNLL-2003-formatted task."}
    )
    labels: Optional[str] = field(
        default=None,
        metadata={"help": "Path to a file containing all labels. If not specified, CoNLL-2003 labels are used."},
    )
    max_seq_length: int = field(
        default=128,
        metadata={
            "help": "The maximum total input sequence length after tokenization. Sequences longer "
            "than this will be truncated, sequences shorter will be padded."
        },
    )
    overwrite_cache: bool = field(
        default=False, metadata={"help": "Overwrite the cached training and evaluation sets"}
    )


# See all possible arguments in src/transformers/training_args.py
# or by passing the --help flag to this script.
# We now keep distinct sets of args, for a cleaner separation of concerns.

parser = HfArgumentParser((ModelArguments, DataTrainingArguments, TrainingArguments))
if sys.argv[1].endswith(".json"):
    # If we pass only one argument to the script and it's the path to a json file,
    # let's parse it to get our arguments.
    model_args, data_args, training_args = parser.parse_json_file(json_file=os.path.abspath(sys.argv[1]))
    # 읽을 문장
else:
    model_args, data_args, training_args = parser.parse_args_into_dataclasses()
# model_args, data_args, training_args = parser.parse_json_file(json_file=os.path.abspath('argument_fashion.json'))

if (
    os.path.exists(training_args.output_dir)
    and os.listdir(training_args.output_dir)
    and training_args.do_train
    and not training_args.overwrite_output_dir
):
    raise ValueError(
        f"Output directory ({training_args.output_dir}) already exists and is not empty. Use --overwrite_output_dir to overcome."
    )

# Setup logging
# logging.basicConfig(
#     format="%(asctime)s - %(levelname)s - %(name)s -   %(message)s",
#     datefmt="%m/%d/%Y %H:%M:%S",
#     level=logging.INFO if training_args.local_rank in [-1, 0] else logging.WARN,
# )
# logger.warning(
#     "Process rank: %s, device: %s, n_gpu: %s, distributed training: %s, 16-bits training: %s",
#     training_args.local_rank,
#     training_args.device,
#     training_args.n_gpu,
#     bool(training_args.local_rank != -1),
#     training_args.fp16,
# )
# logger.info("Training/evaluation parameters %s", training_args)

# Set seed
set_seed(training_args.seed)

# Prepare CONLL-2003 task
labels = get_labels(data_args.labels)
label_map: Dict[int, str] = {i: label for i, label in enumerate(labels)}
num_labels = len(labels)

# Load pretrained model and tokenizer
#
# Distributed training:
# The .from_pretrained methods guarantee that only one local process can concurrently
# download model & vocab.

config = AutoConfig.from_pretrained(
    model_args.config_name if model_args.config_name else model_args.model_name_or_path,
    num_labels=num_labels,
    id2label=label_map,
    label2id={label: i for i, label in enumerate(labels)},
    cache_dir=model_args.cache_dir,
)
tokenizer = AutoTokenizer.from_pretrained(
    model_args.tokenizer_name if model_args.tokenizer_name else model_args.model_name_or_path,
    cache_dir=model_args.cache_dir,
    use_fast=model_args.use_fast,
)
model = AutoModelForTokenClassification.from_pretrained(
    model_args.model_name_or_path,
    from_tf=bool(".ckpt" in model_args.model_name_or_path),
    config=config,
    cache_dir=model_args.cache_dir,
)

# Get datasets
train_dataset = (
    NerDataset(
        data_dir=data_args.data_dir,
        tokenizer=tokenizer,
        labels=labels,
        model_type=config.model_type,
        max_seq_length=data_args.max_seq_length,
        overwrite_cache=data_args.overwrite_cache,
        mode=Split.train,
    )
    if training_args.do_train
    else None
)
eval_dataset = (
    NerDataset(
        data_dir=data_args.data_dir,
        tokenizer=tokenizer,
        labels=labels,
        model_type=config.model_type,
        max_seq_length=data_args.max_seq_length,
        overwrite_cache=data_args.overwrite_cache,
        mode=Split.dev,
    )
    if training_args.do_eval
    else None
)

def align_predictions(predictions: np.ndarray, label_ids: np.ndarray) -> Tuple[List[int], List[int]]:
    preds = np.argmax(predictions, axis=2)

    batch_size, seq_len = preds.shape

    out_label_list = [[] for _ in range(batch_size)]
    preds_list = [[] for _ in range(batch_size)]

    for i in range(batch_size):
        for j in range(seq_len):
            if label_ids[i, j] != nn.CrossEntropyLoss().ignore_index:
                out_label_list[i].append(label_map[label_ids[i][j]])
                preds_list[i].append(label_map[preds[i][j]])

    return preds_list, out_label_list

def compute_metrics(p: EvalPrediction) -> Dict:
    preds_list, out_label_list = align_predictions(p.predictions, p.label_ids)
    return {
        "precision": precision_score(out_label_list, preds_list),
        "recall": recall_score(out_label_list, preds_list),
        "f1": f1_score(out_label_list, preds_list),
    }

# Initialize our Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    compute_metrics=compute_metrics,
)

def return_closest_entity(preds_list, fashion_category_list, sentence_to_predict):
    from collections import defaultdict

    # Edit distance를 적용해서 가장 가까운 entity 탐색
    category_dic = read_category('preprocessing/fashion_category_1012_english.csv')
    category_to_entry = defaultdict(list)
    for k, v in category_dic.items():
        category_to_entry[v].append(k)

    # print(category_to_entry)

    tag_to_entry = {}
    for category in fashion_category_list:
        tag_to_entry[category] = ""

    for i, tag in enumerate(preds_list[0]):
        if tag == 'O':
            continue
        for category in fashion_category_list:
            if category in tag:
                if tag.split('_')[1] == 'B': # start of the tag
                    tag_to_entry[tag.split('_')[0]] += '|' + sentence_to_predict.split()[i]
                else: # I tag
                    tag_to_entry[tag.split('_')[0]] += ' ' + sentence_to_predict.split()[i]

    # 이미지 atrribute에 매칭되도록 dictionary 추가
    attribute_image_match_dic = {
        'Fit': '핏',
        'Pattern': '프린트',
        'Material': '소재',
        'Mood': '스타일',
        'Color': '색상',
        'Neckline': '넥라인',
        'Gender': '성별',
        'Season': '시즌',
    }
    for category in fashion_category_list:
        if category not in attribute_image_match_dic:
            attribute_image_match_dic[category] = '카테고리'


    # 출력시에 attribute_image_match_dic을 통과해서 출력해서 카테고리 이름 변경
    final_dict = defaultdict(list)
    for k, v in tag_to_entry.items():
        if v:
            for entry in v[1:].split('|'):
                min_distance = 999
                to_print = None
                for candidate in category_to_entry[k]:
                    if levenshtein(candidate, entry) < min_distance:
                        to_print = candidate
                        min_distance = levenshtein(candidate, entry)

                final_dict[attribute_image_match_dic[k]].append(to_print)

    return final_dict



@app.route('/home')
def hello():
    return "Hello World"


@app.route('/test')
def test():
    return render_template('post.html')


# Predict
#### 이만큼이 핵심
@app.route('/post', methods=['POST'])
def predict_fashion():
    if request.method == 'POST':
        input_text = request.form['contents_text']
        print(input_text)
        # print(input_text)
        # input_text = open('input.txt', 'r').read()
        import re
        sentence_to_predict = " ".join(re.sub('[^A-Za-z0-9가-힣]', ' ', input_text).split())

        test_dataset = FashionDataset(
            input_sentence=sentence_to_predict,
            tokenizer=tokenizer,
            labels=labels,
            model_type=config.model_type,
            max_seq_length=data_args.max_seq_length,
            overwrite_cache=data_args.overwrite_cache,
            mode=Split.test,
        )

        predictions, label_ids, metrics = trainer.predict(test_dataset)
        preds_list, _ = align_predictions(predictions, label_ids)

        fashion_category_list = ['Gender', 'Pattern', 'Season', 'Fit', 'Color', 'Material', 'Neckline', 'Swimsuit', 'Blouse', 'Bra', 'Cardigan', 'Coat', 'TopBottomSet', 'OnePiece', 'Jacket', 'Leggins', 'Outer', 'Panty', 'Pants', 'Romper', 'Shirt', 'shorts', 'Skirt', 'Tshirt', 'BraPantySet', 'Underwear', 'Top', 'Vest', 'Mood']

        final_entity = return_closest_entity(preds_list=preds_list, fashion_category_list=fashion_category_list, sentence_to_predict=sentence_to_predict)
        # for k, v in final_entity.items():
        #     final_entity[k] = ','.join(v)
        return jsonify(final_entity)

        my_dict = {}
        for category in fashion_category_list:
            my_dict[category]=""

        for i, tag in enumerate(preds_list[0]):
            if tag == 'O':
                continue
            for category in fashion_category_list:
                if category in tag:
                    if tag.split('_')[1] == 'B':
                        my_dict[tag.split('_')[0]] += '|' + sentence_to_predict.split()[i]
                    else:
                        my_dict[tag.split('_')[0]] += ' ' + sentence_to_predict.split()[i]


        parsed_dict = {}
        print(my_dict)
        for k, v in my_dict.items():
            if v:
                parsed_dict[attribute_image_match_dic[k]] = v[1:].split('|')
        return jsonify(parsed_dict)

        """
        parsed_dict = {}
        for k, v in my_dict.items():
            if v:
                parsed_dict[k] = v[1:].split('|')
        return jsonify(parsed_dict)
        """

        """
        return jsonify(
            {
                "tags": [sentence_to_predict.split()[i]+'-'+tag for i, tag in enumerate(preds_list[0])]
            }
        )
        """
        # return jsonify({'sentence': final_sentence})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
