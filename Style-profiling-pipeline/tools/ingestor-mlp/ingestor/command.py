import dataclasses
import functools
import pathlib
import queue

import typer
import yaml
import pydash as py_

from . import config
from . import main
from . import const
from . import database
from . import schema
from . import utils

import logging
from typing import Optional, Tuple


@dataclasses.dataclass
class Record():
    purpose: str = 'none'

@dataclasses.dataclass()
class KFashionRecord(Record):
    style: Optional[pathlib.Path] = None
    image: Optional[pathlib.Path] = None
    annotation: Optional[pathlib.Path] = None

@dataclasses.dataclass()
class TextDemoRecord(Record):
    text: Optional[pathlib.Path] = None
    annotation: Optional[pathlib.Path] = None

class Records(queue.SimpleQueue):
    def put(self, item: Record, block: bool = True, timeout: Optional[float] = None):
        if not isinstance(item, Record):
            raise TypeError(f'item should be Record, but {type(Record)}')

        return super().put(item, block, timeout)


_logger = logging.getLogger(__name__)


def command(dataset_type: const.SupportedDatasetType):
    def wrapper(func):
        @main.app.command(name=dataset_type.value)
        @functools.wraps(func)
        def decorator(*args, **kwargs):
            success_cnt, failed_cnt = func(*args, dataset_type=dataset_type)
            typer.echo(success_cnt)
            typer.echo(failed_cnt)
            return None
        return decorator
    return wrapper


@main.app.command(name='clean')
def clean():

    #
    utils.clean_files()

    #
    for dataset_type in const.SupportedCollection:
        database.get_collection(dataset_type.value).drop()


@command(const.SupportedDatasetType.VERSIONED_IMAGE_TAGGING)
def ingest_versioned_kfashion_to_image_tagging(
    src_path: str = './dataset/K-Fashion-Versioned',
    *, dataset_type: const.SupportedDatasetType = None
) -> Tuple[utils.DatasetCountVersioned, utils.DatasetCountVersioned]:

    def _read_records(purpose, src_path):
        for image in pathlib.Path(src_path, '원천데이터').glob('**/*.*'):
            annotation = pathlib.Path(
                src_path, '라벨링데이터', image.parent.name, image.name
            ).with_suffix('.json')

            style = image.parent.name

            if annotation.exists():
                records.put(KFashionRecord(purpose, style, image, annotation))

    #
    success_cnt = utils.DatasetCountVersioned('Success')
    failed_cnt = utils.DatasetCountVersioned('Failed')

    #
    src_path = pathlib.Path(src_path)

    #
    records = Records()

    #
    typer.echo('searching training dataset...', nl=False)
    _read_records('training', pathlib.Path(src_path, 'Training'))
    typer.echo(f'{records.qsize()}'); t = records.qsize()

    typer.echo('searching validation dataset...', nl=False)
    _read_records('validation', pathlib.Path(src_path, 'Validation'))
    typer.echo(f'{records.qsize() - t}')


    # test
    dataset_id = '634650c8122746be69d4b8d4'
    bundle_id = '6348c7025fcdbdc77fce345e'
    versioned_dataset_name = 'image-tagging-test'

    # info
    versioned_dataset_id = database.upsert_versioned_dataset(versioned_dataset_name, dataset_id, bundle_id, success_cnt)

    #
    while records.qsize():
        record: KFashionRecord = records.get()

        try:
            # check annotation schema
            annotation = yaml.full_load(record.annotation.read_text())
            if not schema.validate_dataset(dataset_type, annotation):
                raise ValueError(f'{annotation}')

            #
            record_id = py_.get(annotation, '이미지 정보.이미지 식별자')

            #
            image_path = utils.copy_file(dataset_id, dataset_type, 'images', record_id, record.image)
            if image_path is None:
                raise ValueError(f'duplicated image: {record.image}')

            #
            annotations = list()
            for label in ['상의', '하의', '원피스', '아우터']:
                rects = py_.get(annotation, f'데이터셋 정보.데이터셋 상세설명.렉트좌표.{label}', [])
                labelings = py_.get(annotation, f'데이터셋 정보.데이터셋 상세설명.라벨링.{label}', [])

                for rect, labeling in zip(rects, labelings):
                    if not(rect) or not(labeling):
                        continue

                    rect_x = py_.get(rect, 'X좌표')
                    rect_y = py_.get(rect, 'Y좌표')
                    rect_w = py_.get(rect, '가로')
                    rect_h = py_.get(rect, '세로')

                    bbox_left, bbox_top = rect_x, rect_y + rect_h
                    bbox_right, bbox_bottom = rect_x + rect_w, rect_y

                    attributes = []
                    for name, values in labeling.items():
                        if isinstance(values, str):
                            values = [values, ]
                        attributes.append({'key': name, 'values': values})

                    annotations.append({
                        'bbox': [bbox_left, bbox_top, bbox_right, bbox_bottom],
                        'label': label,
                        'attributes': attributes
                    })

            #
            image = {
                'name': record.image.name,
                'url': f'/media/{dataset_id}/{image_path}',
            }

            # file_id = image_name
            database.upsert_versioned_data(record.purpose, dataset_id, bundle_id, versioned_dataset_id,
                    file=image, annotations=annotations
                    )

        except Exception as e:
            _logger.debug(f'failed record {record} with exception: {e}')
            failed_cnt.increase(record.purpose)
        else:
            success_cnt.increase(record.purpose)

    database.update_versioned_dataset(versioned_dataset_id, success_cnt)

    return success_cnt, failed_cnt


@command(const.SupportedDatasetType.DATASET_IMAGE_TAGGING)
def ingest_dataset_kfashion_image_to_image_tagging(
    src_path: str = config.ORIGIN_PATH + '/K-Fashion',
    *, dataset_type: const.SupportedDatasetType = None
) -> Tuple[utils.DatasetCount, utils.DatasetCount]:    

    def _read_records(purpose, src_path):
        for image in pathlib.Path(src_path, '원천데이터').glob('**/*.*'):

            style = image.parent.name

            annotation = pathlib.Path(
                src_path, '라벨링데이터', image.parent.name, image.name
            ).with_suffix('.json')

            if annotation.exists():
                records.put(KFashionRecord(purpose, style, image, annotation))

    #
    success_cnt = utils.DatasetCount('Success')
    failed_cnt = utils.DatasetCount('Failed')

    #
    src_path = pathlib.Path(src_path)

    #
    records = Records()

    #    
    typer.echo('searching dataset...', nl=False)
    _read_records('dataset', pathlib.Path(src_path, 'Training'))
    _read_records('dataset', pathlib.Path(src_path, 'Validation'))
    typer.echo(f'{records.qsize()}'); t = records.qsize()    
    
    # dataset 
    dataset_id = database.upsert_dataset('K-Fashion', const.SupportedMltask.IMAGE_TAGGING, '')

    # bundles
    bundles = [ path.name for path in list(pathlib.Path(src_path, 'Training', '원천데이터').iterdir()) ] 
    bundles += [ path.name for path in list(pathlib.Path(src_path, 'Validation', '원천데이터').iterdir()) ] 
    bundles = list(set(bundles))

    bundles_name_id = {}
    for bundle in bundles:
        bundles_name_id[bundle] = database.upsert_bundle(dataset_id, bundle)

    # 
    while records.qsize():
        record: KFashionRecord = records.get()

        try:
            # check annotation schema
            annotation = yaml.full_load(record.annotation.read_text())
            if not schema.validate_dataset(dataset_type, annotation):
                raise ValueError(f'{annotation}')

            #
            record_id = py_.get(annotation, '이미지 정보.이미지 식별자')

            #
            image_path = utils.copy_file(dataset_id, dataset_type, 'images', record_id, record.image)
            if image_path is None:
                raise ValueError(f'duplicated image: {record.image}')

            #
            annotations = list()
            for label in ['상의', '하의', '원피스', '아우터']:
                rects = py_.get(annotation, f'데이터셋 정보.데이터셋 상세설명.렉트좌표.{label}', [])
                labelings = py_.get(annotation, f'데이터셋 정보.데이터셋 상세설명.라벨링.{label}', [])

                for rect, labeling in zip(rects, labelings):
                    if not(rect) or not(labeling):
                        continue

                    rect_x = py_.get(rect, 'X좌표')
                    rect_y = py_.get(rect, 'Y좌표')
                    rect_w = py_.get(rect, '가로')
                    rect_h = py_.get(rect, '세로')

                    bbox_left, bbox_top = rect_x, rect_y + rect_h
                    bbox_right, bbox_bottom = rect_x + rect_w, rect_y

                    attributes = []
                    for name, values in labeling.items():
                        if isinstance(values, str):
                            values = [values, ]
                        attributes.append({'key': name, 'values': values})

                    annotations.append({
                        'bbox': [bbox_left, bbox_top, bbox_right, bbox_bottom],
                        'label': label,
                        'attributes': attributes
                    })            

            image = {
                'name': record.image.name,
                'url': f'/media/{dataset_id}/{image_path}',
            }

            bundle_id = bundles_name_id[record.style]

            #
            database.upsert_file_annotation(dataset_id, bundle_id, file=image, annotations=annotations)

        except Exception as e:
            _logger.debug(f'failed record {record} with exception: {e}')
            failed_cnt.increase()
        else:
            success_cnt.increase()

    return success_cnt, failed_cnt    


@command(const.SupportedDatasetType.VERSIONED_TEXT_TAGGING)
def ingest_versioned_data_to_text_tagging(
    src_path: str = './dataset/Text-Versioned',
    *, dataset_type: const.SupportedDatasetType = None
):
    def _read_records(purpose, src_path):
        for text in pathlib.Path(src_path).glob('*_sentence.*'):
            annotation = pathlib.Path(src_path, text.name.replace('sentence', 'annotation'))

            if annotation.exists():
                records.put(TextDemoRecord(purpose, text, annotation))        

    def non_label_tag(annotation, start, idx):
        non_label_text = ' '.join([ text_label.split(' ')[0] for text_label in annotation[start: idx] ])
        tag_O = {
            'type': 'text',
            'text': non_label_text
        }
        return tag_O

    def label_tag(annotation, idx, dataset_id):
        label_text, label = annotation[idx].split(' ')
        label_id = database.get_labels_id(dataset_id, label.split('_')[0])
        tag_label = {
            'type': 'label',
            'text': label_text,
            'label_id': label_id,
        }
        return tag_label
        
    #
    success_cnt = utils.DatasetCountVersioned('Success')
    failed_cnt = utils.DatasetCountVersioned('Failed')

    #
    src_path = pathlib.Path(src_path)

    #
    records = Records()

    #
    typer.echo('searching training dataset...', nl=False)
    _read_records('training', pathlib.Path(src_path, 'Training'))
    typer.echo(f'{records.qsize()}'); t = records.qsize()

    typer.echo('searching validation dataset...', nl=False)
    _read_records('validation', pathlib.Path(src_path, 'Validation'))
    typer.echo(f'{records.qsize() - t}')

    # test
    dataset_id = '63476fd373911340b5c558c9'
    bundle_id = '6348c7435fcdbdc77fce345f'
    versioned_dataset_name = 'text-tagging-test'
    
    # info
    versioned_dataset_id = database.upsert_versioned_dataset(versioned_dataset_name, dataset_id, bundle_id, success_cnt)

    while records.qsize():
        record: TextDemoRecord = records.get()
    
        try:
            # annotation
            annotation = record.annotation.read_text().split('\n')

            record_id = record.annotation.name 

            file_path = utils.copy_file(dataset_id, dataset_type, 'text', record_id, record.text)

            if file_path is None:
                raise ValueError(f'duplicated image: {record.text}')

            #
            idx_label = []
            for idx in range(len(annotation)):
                try:
                    label = annotation[idx].split(' ')[1]

                    if label != 'O':
                        idx_label.append(idx)
                except:
                    pass

            annotations = list()
            start = 0
            for idx in idx_label:

                if start < idx_label[-1]:

                    if start != idx:
                        #
                        tag_O = non_label_tag(annotation, start, idx)
                        annotations.append(tag_O)

                        #
                        tag_label = label_tag(annotation, idx, dataset_id)
                        annotations.append(tag_label)

                        start = idx + 1
                    else:

                        tag_label = label_tag(annotation, idx, dataset_id)
                        annotations.append(tag_label)                        

                else:

                    tag_O = non_label_tag(annotation, start + 1, len(annotation))
                    annotations.append(tag_O)

            sentence = {
                'name': record.text.name,
                'url': f'/media/{dataset_id}/{file_path}',
            }
            
            database.upsert_versioned_data(record.purpose, dataset_id, bundle_id, versioned_dataset_id, 
                    file=sentence, annotations=annotations
            )

        except Exception as e:
            _logger.debug(f'failed record {record} with exception: {e}')
            failed_cnt.increase(record.purpose)
        else:
            success_cnt.increase(record.purpose)

    database.update_versioned_dataset(versioned_dataset_id, success_cnt)
    return success_cnt, failed_cnt


@command(const.SupportedDatasetType.DATASET_TEXT_TAGGING)
def ingest_dataset_data_to_text_tagging(
    src_path: str = config.ORIGIN_PATH + '/TextTagging',
    *, dataset_type: const.SupportedDatasetType = None
):

    def non_label_tag(text):
        tag_O = {
            'type': 'text',
            'text': text
        }
        return tag_O

    def label_tag(text, tag, dataset_id):
        label_id = database.get_labels_id(dataset_id, tag.split('_')[0])
        tag_label = {
            'type': 'label',
            'text': text,
            'label_id': label_id,
        }
        return tag_label
        
    def sentence_parse(sentence_tag):
        sentence = []
        for word_tag in sentence_tag:
            word, tag = word_tag.split(' ')
            sentence.append(word)

            if tag == 'O':
                annotations.append(non_label_tag(word))
            else:
                annotations.append(label_tag(word, tag, dataset_id))
        sentence = ' '.join(sentence)
        return sentence, annotations

    #
    success_cnt = utils.DatasetCount('Success')
    failed_cnt = utils.DatasetCount('Failed')

    # dataset
    dataset_id = database.upsert_dataset('TextTagging', const.SupportedMltask.TEXT_TAGGING, '')

    # bundle
    bundle_id = database.upsert_bundle(dataset_id, '의류')

    #
    for file_name in ['train.txt', 'dev.txt', 'test.txt']:
        #        
        data_path = pathlib.Path(src_path, file_name)

        with open(data_path, 'r') as file:
            data = file.read().splitlines()
            sentence_separate_indexes = [ idx for idx, text in enumerate(data) if text == '']

            #
            for i in range(len(sentence_separate_indexes)):
                
                try:
                    idx = sentence_separate_indexes[i]

                    annotations = list()

                    #
                    if i == 0:
                        sentence_tag = data[0: idx]
                    else:
                        sentence_tag = data[sentence_separate_indexes[i-1]+1: sentence_separate_indexes[i]]

                    sentence, annotations = sentence_parse(sentence_tag)

                    # copy
                    dst = pathlib.Path(config.FS_BASE_PATH, dataset_id, f'{i}_{file_name}')
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    with open(dst, 'w') as new_file:
                        new_file.write(sentence)
                    
                    #
                    text = {
                        'name': f'{i}_{file_name}',
                        'url': f'/media/{dataset_id}/{i}_{file_name}'
                    }

                    #
                    database.upsert_file_annotation(dataset_id, bundle_id, file=text, annotations=annotations)

                except Exception as e:
                    _logger.debug(f'failed record with exception: {e}')
                    failed_cnt.increase()
                else:
                    success_cnt.increase()

    return success_cnt, failed_cnt    

