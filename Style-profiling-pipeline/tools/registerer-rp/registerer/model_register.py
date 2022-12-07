# import logging
import docker

from typing import Optional

from .main import app
from .database import ModelDatabase
from .config import WIDE_DEEP, NCF


@app.command(name='clean')
def clean_for_debug():
    db = ModelDatabase()
    client = docker.from_env()
    db.db.drop_collection('models')
    client.images.remove('wide_deep:latest')


@app.command()
def wide_deep(
    dockerfile: Optional[str] = WIDE_DEEP['base_path']['dockerfile'],
    image_name: Optional[str] = 'wide_deep:latest'):

    db = ModelDatabase('Wide and Deep')
    db.upsert(image_name)

    client = docker.from_env()
    _, build_log = client.images.build(path=dockerfile, tag=image_name, rm=True)


@app.command()
def ncf(
    dockerfile: Optional[str] = NCF['base_path']['dockerfile'],
    image_name: Optional[str] = 'ncf:latest'):    

    db = ModelDatabase('Neural Collaborative Filtering')
    db.upsert(image_name)

    client = docker.from_env()
    _, build_log = client.images.build(path=dockerfile, tag=image_name, rm=True)
    