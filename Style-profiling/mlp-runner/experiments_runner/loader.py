import collections
import pathlib
import json
import io
from this import d
from unittest import loader

import pydash as py_
import yaml
import PIL.Image

from . import const
from . import config
from . import database

import logging
from typing import Iterable, Mapping, List, Tuple, Callable, Optional


class NotSupportedLoader(BaseException):
    pass


_logger = logging.getLogger(__name__)


def _load_image_to_yolov5(examples: Iterable[Mapping], target_dir: pathlib.Path) -> None:

    split_purpose = ['training', 'validation', 'testing']

    #
    target_dir = pathlib.Path(config.FS_BASE_PATH_EXPERIMENTS, target_dir)
    for purpose in split_purpose:
        pathlib.Path(target_dir, 'images', purpose).mkdir(parents=True, exist_ok=True)
        pathlib.Path(target_dir, 'labels', purpose).mkdir(parents=True, exist_ok=True)

    #
    count = collections.defaultdict(int, {'training': 0, 'validation': 0, 'testing': 0})

    objects = []
    for example in examples:

        coordinates = list()

        #
        split = py_.get(example, 'split')
        purpose = split_purpose[split]

        #
        file_id = py_.get(example, 'file_id')
        image_example = database.get_file(file_id)

        image_name = py_.get(image_example, 'name')
        image_url = py_.get(image_example, 'url')
        image_url = pathlib.Path(image_url).relative_to('/media').parent
        image_src = pathlib.Path(config.MEDIA_ROOT, image_url, image_name)

        #
        image_dst = pathlib.Path(target_dir, 'images', purpose, image_src.name)
        image_dst.write_bytes(
            image_src.read_bytes()
        )

        #
        im = PIL.Image.open(image_src)
        width, height = im.size
        #
        annotations = py_.get(example, 'labels')

        for annotation in annotations:
            label = py_.get(annotation, 'label')
            
            left, top, right, bottom = py_.get(annotation, 'bbox')
            center_x = (right - left)/2
            center_y = -1*(top - bottom)/2
            w = right - left
            h = -1*(top - bottom)

            if label not in objects:
                objects.append(label)

            obj_index = objects.index(label)
            coordinates.append(tuple([
                obj_index,
                center_x/width,
                center_y/height,
                w/width,
                h/height,
            ]))


        if not coordinates:
            continue

        # 
        label_dst = pathlib.Path(target_dir, 'labels', purpose, image_src.stem).with_suffix('.txt')
        label_dst.write_text(
            '\n'.join([
                '{0:<2} {1:0.6f} {2:0.6f} {3:0.6f} {4:0.6f}'.format(*coordinate) for coordinate in coordinates
            ]) + '\n'
        )

        #
        count[purpose] += 1


    # .yaml은 로컬 데이터셋 폴더가 컨테이너 내의 usr/src/datasets에 마운트된다고 가정한 상태.
    dataset_yaml = {
        'path': '../datasets',
        'train': 'images/training' if count['training'] > 0 else None,
        'val': 'images/validation' if count['validation'] > 0 else None,

        'nc': len(objects),
        'names': objects,
    }

    dataset_path = pathlib.Path(target_dir, 'dataset.yaml')
    dataset_path.write_text(
        yaml.dump(dataset_yaml, allow_unicode=True)
    )

    objects.insert(0, '__background__')
    index_to_name = dict(enumerate(objects))
    index_to_name_path = pathlib.Path(target_dir, 'index_to_name.json')
    index_to_name_path.write_text(json.dumps(index_to_name, ensure_ascii=False))

    #
    _logger.info('{:-^80}'.format(' dataset counts'))
    _logger.info(', '.join([f'{k}: {v}' for k, v in count.items()]))


def _load_image_to_image_tagging_classifier(examples: Iterable[Mapping], target_dir: pathlib.Path):

    split_purpose = ['training', 'validation', 'testing']

    #
    _SEPARATOR_NAME_TO_VALUE = '::'

    #
    target_dir = pathlib.Path(config.FS_BASE_PATH_EXPERIMENTS, target_dir)
    for purpose in split_purpose:
        pathlib.Path(target_dir, purpose, 'images').mkdir(parents=True, exist_ok=True)
        pathlib.Path(target_dir, purpose, 'labels').mkdir(parents=True, exist_ok=True)

    #    
    count = collections.defaultdict(int, {'training': 0, 'validation': 0, 'testing': 0})

    classes = []

    for example in examples:
        
        #
        split = py_.get(example, 'split')
        purpose = split_purpose[split]
        
        #
        annotations = py_.get(example, 'labels')

        labels = dict()
        for annotation in annotations:
            left, top, right, bottom = py_.get(annotation, 'bbox')
            # start_x, start_y, end_x, end_y = left, bottom, right, top

            attributes = py_.get(annotation, 'attributes')
            
            label_indices = list()

            # 
            for attribute in attributes:
                property = py_.get(attribute, 'key')
                values = py_.get(attribute, 'values')

                for value in values:
                    class_name = _SEPARATOR_NAME_TO_VALUE.join([property, value])

                    if class_name not in classes:
                        classes.append(class_name)
                    
                    class_index = classes.index(class_name)
                    label_indices.append(class_index)

                if not label_indices:
                    continue

            #
            # labels[(start_x, start_y, end_x, end_y)] = label_indices
            labels[(left, top, right, bottom)] = label_indices

        if not labels:
            continue

        #
        file_id = py_.get(example, 'file_id')
        image_example = database.get_file(file_id)


        image_name = py_.get(image_example, 'name')

        image_url = py_.get(image_example, 'url')
        image_url = pathlib.Path(image_url).relative_to('/media').parent
        image_src = pathlib.Path(config.MEDIA_ROOT, image_url, image_name)

        #
        im = PIL.Image.open(io.BytesIO(image_src.read_bytes()))

        for bbox, label_indices in labels.items():
            filename = f'{image_src.stem}-{id(bbox)}{image_src.suffix}'
            image_dst = pathlib.Path(target_dir, purpose, 'images', filename)

            im.crop(bbox).save(image_dst)

            #
            label_dst = pathlib.Path(target_dir, purpose, 'labels', filename).with_suffix('.json')
            label_dst.write_text(json.dumps({
                'labels': label_indices
            }))            

            count[purpose] += 1

    dataset_yaml = {
        'path': '../datasets',
        'train': 'training' if count['training'] > 0 else None,
        'val': 'validation' if count['validation'] > 0 else None,

        'nc': len(classes),
        'names': classes,
    }

    dataset_path = pathlib.Path(target_dir, 'dataset.yaml')
    dataset_path.write_text(
        yaml.dump(dataset_yaml, allow_unicode=True)
    )

    index_to_name = dict(enumerate(classes))
    index_to_name_path = pathlib.Path(target_dir, 'index_to_name.json')
    index_to_name_path.write_text(json.dumps(index_to_name, ensure_ascii=False))

    #
    _logger.info('{:-^80}'.format(' dataset counts'))
    _logger.info(', '.join([f'{k}: {v}' for k, v in count.items()]))
    

def _load_text_to_koelectra_base(examples: Iterable[Mapping], target_dir: pathlib.Path) -> None:

    split_purpose = ['train', 'dev', 'test']
    #
    
    target_dir = pathlib.Path(config.FS_BASE_PATH_EXPERIMENTS, target_dir)

    pathlib.Path(target_dir).mkdir(parents=True, exist_ok=True)

    count = collections.defaultdict(int, {'train': 0, 'dev': 0, 'test': 0})

    # 
    for file in ['train', 'dev', 'test', 'labels']:
        with open(pathlib.Path(target_dir, f'{file}.txt'), 'w') as f:
            pass

    labels = []
    for example in examples:
        annotation = py_.get(example, 'labels')
        split = py_.get(example, 'split')
        purpose = split_purpose[split]

        tags = []
        checkpoint_B_I = 0
        for item in annotation:
            if item['type'] == 'text':
                text_ls = item['text'].rstrip().lstrip().split(' ')
                text_label_ls = [ text + ' ' + 'O' for text in text_ls ]
                tags.append(text_label_ls)
                
                checkpoint_B_I = 0

            elif item['type'] == 'label':
                text = item['text']
                label_id = item['label_id']
                label_name = database.get_label_name(label_id)

                if checkpoint_B_I == 0:
                    label_B_I = label_name + '_B'
                    text_label = [ text + ' ' + label_B_I]
                    tags.append(text_label)
                    labels.append(label_B_I)

                else:
                    label_B_I = label_name + '_I'
                    text_label = [ text + ' ' + label_B_I]
                    tags.append(text_label)               
                    labels.append(label_B_I)     

            else:
                pass
        
        flatten_tags = [ item for ls in tags for item in ls ]

        # write list to file
        with open(pathlib.Path(target_dir, f'{purpose}.txt'), 'w') as f:
            for item in flatten_tags:
                f.write(f'{item}\n')

            f.write(f'\n')

        count[purpose] += 1

    with open(pathlib.Path(target_dir, f'labels.txt'), 'w') as f:
        for item in list(set(labels)):
            f.write(f'{item}\n')



    train_argument_json = {
        "model_name_or_path": "monologg/koelectra-base-v2-discriminator",
        "data_dir": "../datasets/",
        "output_dir": "./results/",
        "labels": "../datasets/labels.txt",
        "max_seq_length": 512,
        "num_train_epochs": 5,
        "per_device_train_batch_size": 8,
        "do_train": True if count['train'] > 0 else False,
        "do_predict": True if count['test'] > 0 else False,
        "do_eval": True if count['dev'] > 0 else False,
        "seed": 1,
        "logging_dir": './exp_results',
        "logging_steps": 50        
    }

    train_argument_path  = pathlib.Path(target_dir, 'train_argument.json')

    with open(train_argument_path, 'w') as f:
        json.dump(train_argument_json, f, indent = 4)

    _logger.info(', '.join([f'{k}: {v}' for k, v in count.items()]))


def get_loader_target_dir_root(experiment: database.Experiment) -> pathlib.Path:
    return pathlib.Path(str(experiment._id), 'datasets')


_LOADER_MAP={
    'Yolov5(small)': _load_image_to_yolov5,
    'Yolov5(medium)': _load_image_to_yolov5,
    'Classifier(resnet50)': _load_image_to_image_tagging_classifier,
    'Classifier(resnet101)': _load_image_to_image_tagging_classifier,
    'Koelectra(base)': _load_text_to_koelectra_base,
}


def get_loaders(experiment: database.Experiment, target_dir_root: Optional[pathlib.Path] = None) -> List[Callable]:

    def _factory(func, examples, target_dir):
        return lambda: func(examples, target_dir)

    def update_status(experiment, name, target_dir):
        return lambda: database.update_experiment_artifacts(experiment._id, name, 'loader_dir', str(target_dir))

    #
    if target_dir_root is None:
        target_dir_root = get_loader_target_dir_root(experiment)
    
    algorithms = py_.get(experiment, 'algorithms')

    loaders = []

    for algorithm in algorithms:
        name = algorithm['name']
        func = _LOADER_MAP[name]

        if func is None:
            raise NotSupportedLoader(f'not supported types: {name}')

        examples = database.get_annotation(experiment.versioned_dataset_id)
        target_dir = pathlib.Path(target_dir_root, config.LOADER_DIR[name])

        loaders.append(_factory(func, examples, target_dir))
        loaders.append(update_status(experiment, name, target_dir))  

    return loaders
