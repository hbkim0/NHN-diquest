import dataclasses
import enum
import pathlib
import datetime

import bson
import pymongo
import pymongo.collection
import pymongo.cursor
import pymongo.errors
import pydash as py_

from . import config
from . import mlflow_api

import logging
from typing import Any, Mapping, List, Optional, Union


_DATABASE_NAME = 'mamihlapinatapai_rp'
_COLLECTION_NAME_EXPERIMENT = 'experiments'
_COLLECTION_NAME_PRODUCT = 'products'
_COLLECTION_NAME_HISTORY = 'historys'
_COLLECTION_NAME_CUSTOMER = 'customers'
_COLLECTION_NAME_MODELS = 'models'



class ExperimentStatus(enum.Enum):
    CREATED = 0
    QUEUED = 1
    TRAINING = 2
    DONE = 3
    FAILED = 4


_logger = logging.getLogger(__name__)
_mongo_client: pymongo.MongoClient = None


@dataclasses.dataclass
class Experiment():
    _id: bson.ObjectId
    model_id: str
    parameters: list


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


def update_experiment_time(experiment_id, field):
    #
    if not bson.ObjectId.is_valid(experiment_id):
        return False

    #
    collection = get_collection()
    result = collection.update_one(
        {'_id': bson.ObjectId(experiment_id)},
        {'$set': {f'{field}': datetime.datetime.utcnow()}},
    )

    return result.modified_count == 1        


def update_experiment_status(experiment_id, status: ExperimentStatus) -> bool:
    #
    collection = get_collection()
    result = collection.update_one(
        {'_id': bson.ObjectId(experiment_id)},
        {'$set': {'status': status.value}},
    )

    return result.modified_count == 1


def update_experiment_metric(experiment_id):

    metric = mlflow_api.get_metric(experiment_id)

    collection = get_collection()
    result = collection.update_one(
        {'_id': bson.ObjectId(experiment_id)},
        {'$set': {'rmse': metric}},
    )    
    return result.modified_count == 1


def update_experiment_serving(new_exp_id, old_exp_id):

    collection = get_collection()

    if old_exp_id is not None:
        #
        collection.update_one(
            {'_id': bson.ObjectId(old_exp_id)},
            {'$set': {'serving': 0}},
        ) 
    else:
        pass

    collection.update_one(
        {'_id': bson.ObjectId(new_exp_id)},
        {'$set': {'serving': 1}},
    )


def get_model(_id):
    filter={'_id': bson.ObjectId(_id)}
    collection = get_collection(_COLLECTION_NAME_MODELS, _DATABASE_NAME)
    return collection.find_one(filter) 
    

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
        model_id=experiment['model_id'],
        parameters=experiment['parameters'],
    )


def get_data():
    collection = get_collection(_COLLECTION_NAME_HISTORY, _DATABASE_NAME)

    stage_lookup_product = {
        '$lookup': {
            'from': 'products', 
            'localField': 'product', 
            'foreignField': 'identifier', 
            'as': 'product_doc'
        }
    }

    stage_unset_fields =  {
        '$unset': [
            'ext', 'history', 'mod_date', 'mod_id', 'reg_date', 
            'reg_id', 'product_doc._id', 'product_doc.identifier', 
            'product_doc.description', 'product_doc.ext', 
            'product_doc.history', 'product_doc.image', 
            'product_doc.mod_id', 'product_doc.mod_date', 
            'product_doc.name', 'product_doc.reg_id', 'product_doc.reg_date'
        ]
    }

    stage_lookup_customer = {
        '$lookup': {
            'from': 'customers', 
            'localField': 'customer', 
            'foreignField': 'identifier', 
            'as': 'customer_doc'
        }
    }

    stage_unset_fields_2 = {
        '$unset': [
            'customer_doc._id', 'customer_doc.identifier', 'customer_doc.description', 'customer_doc.ext', 'customer_doc.history', 'customer_doc.image', 'customer_doc.mod_id', 'customer_doc.mod_date', 'customer_doc.name', 'customer_doc.reg_id', 'customer_doc.reg_date'
        ]
    }

    pipeline = [
        stage_lookup_product,
        stage_unset_fields,
        stage_lookup_customer,
        stage_unset_fields_2
    ]

    return collection.aggregate(pipeline)


