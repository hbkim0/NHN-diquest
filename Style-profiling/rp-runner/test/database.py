import dataclasses
import enum
import pathlib

import bson
import pymongo
import pymongo.collection
import pymongo.cursor
import pymongo.errors
import pydash as py_

import config

import logging
from typing import Any, Mapping, List, Optional, Union


_DATABASE_NAME = 'mamihlapinatapai_rp'
_COLLECTION_NAME_EXPERIMENT = 'experiments'
_COLLECTION_NAME_PRODUCT = 'products'
_COLLECTION_NAME_CUSTOMER = 'customers'
_COLLECTION_NAME_HISTORY = 'historys'




class ExperimentStatus(enum.Enum):
    CREATED = 0
    QUEUED = 1
    TRAINING = 2
    DONE = 3
    FAILED = 4


@dataclasses.dataclass
class Experiment():
    _id: bson.ObjectId
    dataset_id: str
    model_id: str
    versioned_dataset_id: str
    algorithms: list

    

_logger = logging.getLogger(__name__)
_mongo_client: pymongo.MongoClient = None


def _get_mongo_client() -> pymongo.MongoClient:

    #
    global _mongo_client
    if isinstance(_mongo_client, pymongo.MongoClient):
        return _mongo_client

    #
    app_name = 'experiments_runner'
    if app_name not in config.DATABASES:
        raise Exception(f'Not found database configuration for {app_name} : {config.DATABASES}')

    if 'CLIENT' not in config.DATABASES[app_name]:
        raise Exception(f'Not found client information for database : {config.DATABASES[app_name]}')
    client_config = config.DATABASES[app_name]['CLIENT']

    #
    params = {
        'host': client_config.get('host', ''),
        'port': client_config.get('port', 27017)
    }
    if ('username' in client_config) and ('password' in client_config):
        params['username'] = client_config['username']
        params['password'] = client_config['password']
    client = pymongo.MongoClient(**params)

    try:
        client.admin.command('ping')
    except pymongo.errors.ConnectionFailure as e:
        _logger.error(f'Server not available(params: {params})')
        raise e
    _logger.info(f'server info: ${client.server_info()}')

    #
    _mongo_client = client
    return client


def get_collection(
    collection_name: Optional[str] = None,
    database_name: Optional[str] = None
) -> pymongo.collection.Collection:

    #
    if database_name is None:
        database_name = _DATABASE_NAME

    #
    if collection_name is None:
        collection_name = _COLLECTION_NAME_EXPERIMENT

    #
    client = _get_mongo_client()
    db = client[database_name]
    return db[collection_name]


def get_product(identifier):
    filter = {'identifier': identifier}
    collection = get_collection(_COLLECTION_NAME_PRODUCT, _DATABASE_NAME)
    return collection.find_one(filter)

def get_customer(identifier):
    filter = {'identifier': identifier}
    collection = get_collection(_COLLECTION_NAME_CUSTOMER, _DATABASE_NAME)
    return collection.find_one(filter)

def get_history():
    collection = get_collection(_COLLECTION_NAME_HISTORY, _DATABASE_NAME)
    return collection.find()