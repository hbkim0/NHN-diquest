import dataclasses
import enum
import pathlib

import bson
import pymongo
import pymongo.collection
import pymongo.cursor
import pymongo.errors
import pydash as py_

from . import config

import logging
from typing import Any, Mapping, List, Optional, Union


_DATABASE_NAME = 'mamihlapinatapai'
_COLLECTION_NAME_EXPERIMENT = 'experiments'
_COLLECTION_NAME_FILE = 'files'
_COLLECTION_NAME_ANNOTATION = 'annotations'
_COLLECTION_NAME_LABELS = 'labels'
_COLLECTION_NAME_MODELS = 'models'



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


def get_experiment(
    current_status: ExperimentStatus = ExperimentStatus.QUEUED,
    next_status: ExperimentStatus = ExperimentStatus.TRAINING
) -> Optional[Experiment]:

    #
    collection = get_collection()
    experiment = collection.find_one_and_update(
        {'status': current_status.value},
        {'$set': {'status': next_status.value}},
        sort=[('_id', 1), ]
    )

    if experiment is None:
        return None

    #
    return Experiment(
        _id=experiment['_id'],
        dataset_id=experiment['dataset_id'],
        model_id=experiment['model_id'],
        versioned_dataset_id=experiment['versioned_dataset_id'],
        algorithms=experiment['algorithms'],
    )


def update_experiment_status(experiment_id: Union[str, bson.ObjectId], status: ExperimentStatus) -> bool:

    #
    if not bson.ObjectId.is_valid(experiment_id):
        return False

    #
    collection = get_collection()
    result = collection.update_one(
        {'_id': bson.ObjectId(experiment_id)},
        {'$set': {'status': status.value}},
    )

    return result.modified_count == 1


def update_experiment_artifacts(experiment_id: Union[str, bson.ObjectId], name: str, type_: str, path: str) -> bool:

    #
    if not bson.ObjectId.is_valid(experiment_id):
        return False

    #
    path = str(pathlib.Path(config.FS_BASE_PATH_EXPERIMENTS, path))

    #
    collection = get_collection()
    result = collection.update_one(
        {'_id': bson.ObjectId(experiment_id), 'artifacts.algorithm_name': name},
        {'$set': {f'artifacts.$.{type_}': path}}
    )
    
    return result.modified_count == 1


def create_experiment_artifacts(experiment: Union[str, bson.ObjectId]) -> bool:
    
    if not bson.ObjectId.is_valid(experiment._id):
        return False    
    
    ls_doc = []
    for algorithm in experiment.algorithms:
        doc = {}
        doc['algorithm_name'] = algorithm['name']
        doc['loader_dir'] = ''
        doc['tensorboard_logdir'] = ''
        ls_doc.append(doc)

    #
    collection = get_collection()

    #
    result = collection.update_one(
        {'_id': bson.ObjectId(experiment._id)},
        {'$set': {'artifacts': ls_doc }}, upsert=True
    )
    return result.modified_count == 1    
    

def get_file(_id):
    filter = {'_id': bson.ObjectId(_id)}
    collection = get_collection(_COLLECTION_NAME_FILE, _DATABASE_NAME)
    return collection.find_one(filter)

def get_annotation(_id):
    filter = {'versioned_dataset_id': _id}
    collection = get_collection(_COLLECTION_NAME_ANNOTATION, _DATABASE_NAME)
    return collection.find(filter)

def get_label_name(_id):
    filter = {'_id': bson.ObjectId(_id)}
    collection = get_collection(_COLLECTION_NAME_LABELS, _DATABASE_NAME)    
    return collection.find_one(filter)['name']

def get_models(_id):
    filter = {'_id': bson.ObjectId(_id)}
    collection = get_collection(_COLLECTION_NAME_MODELS, _DATABASE_NAME)    
    return collection.find_one(filter)