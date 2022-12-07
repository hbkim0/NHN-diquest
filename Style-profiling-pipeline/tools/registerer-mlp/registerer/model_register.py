# import logging
import docker

from typing import Optional

from .main import app
from .database import AlgorithmDatabase
from .config import Yolov5, IMAGE_TAGGING_CLASSIFIER, KOELECTRA


@app.command(name='clean')
def clean_for_debug():
    db = AlgorithmDatabase()
    client = docker.from_env()
    db.db.drop_collection('algorithms')
    client.images.remove('yolov5:latest')
    client.images.remove('classifier_resnet50:latest')
    client.images.remove('classifier_resnet101:latest')
    client.images.remove('koelectra_base:latest')

@app.command()
def yolov5(
    dockerfile: Optional[str] = Yolov5['default_path']['dockerfile'],
    image_name: Optional[str] = 'yolov5:latest',
    cfg_path: Optional[str] = Yolov5['default_path']['cfg_path']):

    db = AlgorithmDatabase('Yolov5')

    db.upsert(image_name, cfg_path=cfg_path)
    client = docker.from_env()
    _, build_log = client.images.build(path=dockerfile, tag=image_name, rm=True)


@app.command()
def image_tagging_classifier_resnet50(
    dockerfile: Optional[str] = IMAGE_TAGGING_CLASSIFIER['resnet50_path']['dockerfile'],
    image_name: Optional[str] = 'classifier_resnet50:latest'):

    db = AlgorithmDatabase('Classifier(resnet50)')
    db.upsert(image_name)

    client = docker.from_env()
    _, build_log = client.images.build(path=dockerfile, tag=image_name, rm=True)


@app.command()
def image_tagging_classifier_resnet101(
    dockerfile: Optional[str] = IMAGE_TAGGING_CLASSIFIER['resnet101_path']['dockerfile'],
    image_name: Optional[str] = 'classifier_resnet101:latest'):

    db = AlgorithmDatabase('Classifier(resnet101)')
    db.upsert(image_name)

    client = docker.from_env()
    _, build_log = client.images.build(path=dockerfile, tag=image_name, rm=True)


@app.command()
def koelectra_base(
    dockerfile: Optional[str] = KOELECTRA['base_path']['dockerfile'],
    image_name: Optional[str] = 'koelectra_base:latest'):

    db = AlgorithmDatabase('Koelectra(base)')
    db.upsert(image_name)

    client = docker.from_env()
    _, build_log = client.images.build(path=dockerfile, tag=image_name, rm=True)


    