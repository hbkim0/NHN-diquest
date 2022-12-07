import collections
import dataclasses
import datetime
import bson

import pymongo
import pymongo.collection
import pymongo.errors

from . import const
from . import config
from . import schema
from . import utils

import logging


_DATABASE_NAME = 'mamihlapinatapai'
_DATASET_COLLECTION_NAME = 'datasets'
_BUNDLES_COLLECTION_NAME = 'bundles'
_FILES_COLLECTION_NAME = 'files'
_ANNOTATIONS_COLLECTION_NAME = 'annotations'
_LABELS_COLLECTION_NAME = 'labels'
_VERSIONED_DATASET_COLLECTION_NAME = 'versioned_datasets'


logger = logging.getLogger(__name__)
_mongo_client: pymongo.MongoClient = None


def _get_mongo_client() -> pymongo.MongoClient:

    #
    global _mongo_client
    if isinstance(_mongo_client, pymongo.MongoClient):
        return _mongo_client

    #
    app_name = 'ingestor'
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
        logger.error(f'Server not available(params: {params})')
        raise e
    logger.info(f'server info: ${client.server_info()}')

    #
    _mongo_client = client
    return client


def get_collection(collection_name):

    #
    if not collection_name:
        raise ValueError(f'not supported collection_name: {collection_name}')

    #
    client = _get_mongo_client()
    db = client[_DATABASE_NAME]
    return db[collection_name]


def upsert_dataset(name, ml_task, cover_image):

    doc = {
        'name': name,
        'description': '',
        'ml_task': ml_task.value,
        'cover_image': cover_image,
        'max_index': 0,
        
        #
        'history': {},
        'ext': {},
        'reg_date': datetime.datetime.utcnow(),
        'reg_id': 'user_id',
        'mod_date': datetime.datetime.utcnow(),
        'mod_id': 'user_id',        
    }

    collection = get_collection(_DATASET_COLLECTION_NAME)
    update_result = collection.update_one(
        {'name': name},
        {'$setOnInsert': doc}, 
        upsert=True        
    )

    return str(update_result.upserted_id)


def upsert_bundle(dataset_id, bundle_name):

    doc = {
        'dataset_id': dataset_id,
        'name': bundle_name,
        'description': '',
        'attributes': [],

        #
        'history': {},
        'ext': {},
        'reg_date': datetime.datetime.utcnow(),
        'reg_id': 'user_id',
        'mod_date': datetime.datetime.utcnow(),
        'mod_id': 'user_id',      
    }

    collection = get_collection(_BUNDLES_COLLECTION_NAME)
    update_result = collection.update_one(
        {'name': bundle_name},
        {'$setOnInsert': doc}, 
        upsert=True        
    )

    return str(update_result.upserted_id)

    
def upsert_file_annotation(dataset_id, bundle_id, **src):

    #
    file_doc = {
        'dataset_id': dataset_id,
        'description': '',
        'bundle_id': bundle_id, 
        'versioned_dataset_id': '',
        'url': src['file']['url'],
        'name': src['file']['name'],
        
        #
        'history': {},
        'ext': {},
        'reg_date': datetime.datetime.utcnow(),
        'reg_id': 'user_id',
        'mod_date': datetime.datetime.utcnow(),
        'mod_id': 'user_id',
    }

    #
    collection = get_collection(_FILES_COLLECTION_NAME)
    update_result = collection.update_one({'url': src['file']['url']}, {'$setOnInsert': file_doc}, upsert=True)

    #
    annotation_doc = {
        'dataset_id': dataset_id,
        'bundle_id': bundle_id,
        'file_id': str(update_result.upserted_id),
        'versioned_dataset_id': '',
        'description': '',
        'done': 1,
        'split': None,
        'labels': src['annotations'], 

        #
        'history': {},
        'ext': {},
        'reg_date': datetime.datetime.utcnow(),
        'reg_id': 'user_id',
        'mod_date': datetime.datetime.utcnow(),
        'mod_id': 'user_id',        
    }

    #
    collection = get_collection(_ANNOTATIONS_COLLECTION_NAME)
    update_result = collection.update_one(
        {'file_id': str(update_result.upserted_id)}, 
        {'$setOnInsert': annotation_doc}, 
        upsert=True
    )   

    return None


def upsert_versioned_data(purpose, dataset_id, bundle_id, versioned_dataset_id, **src):

    purpose_split = {'training': 0, 'validation': 1, 'testing': 2}

    # file documnet
    file_doc = {
        'dataset_id': dataset_id,
        'description': '',
        'bundle_id': bundle_id, 
        'versioned_dataset_id': versioned_dataset_id,
        'url': src['file']['url'],
        'name': src['file']['name'],
        #
        'history': {},
        'ext': {},
        'reg_date': datetime.datetime.utcnow(),
        'reg_id': 'user_id',
        'mod_date': datetime.datetime.utcnow(),
        'mod_id': 'user_id',
    }
    collection = get_collection(_FILES_COLLECTION_NAME)
    update_result = collection.update_one({'url': src['file']['url']}, {'$setOnInsert': file_doc}, upsert=True)

    # annotation document
    anno_doc = {
        'dataset_id': dataset_id,
        'bundle_id': bundle_id,
        'file_id': str(update_result.upserted_id),
        'versioned_dataset_id': versioned_dataset_id,
        'description': '',
        'done': 1,
        'split': purpose_split[purpose],
        'labels': src['annotations'], 
    }

    #
    collection = get_collection(_ANNOTATIONS_COLLECTION_NAME)
    update_result = collection.update_one(
        {'versioned_dataset_id': versioned_dataset_id, 'name': src['file']['name']}, 
        {'$setOnInsert': anno_doc}, 
        upsert=True
    )

    #
    return update_result.upserted_id is not None


def get_labels_id(dataset_id, name):
    collection = get_collection(_LABELS_COLLECTION_NAME)

    # find
    find_result = collection.find_one({'dataset_id': dataset_id, 'name': name})

    if find_result:
        return str(find_result['_id'])
    else:
        doc = {
            'dataset_id': dataset_id,
            'name': name,
            'color': '#CC3D3D',
            #
            'history': {},
            'ext': {},
            'reg_date': datetime.datetime.utcnow(),
            'reg_id': 'user_id',
            'mod_date': datetime.datetime.utcnow(),
            'mod_id': 'user_id',
        }
        
        update_result = collection.update_one({'dataset_id': dataset_id, 'name': name}, {'$setOnInsert': doc}, upsert=True)

        return str(update_result.upserted_id)


def upsert_versioned_dataset(versioned_dataset_name, dataset_id, bundle_id, dataset_count):

    collection = get_collection(_VERSIONED_DATASET_COLLECTION_NAME)
    find_result = collection.find_one({'name': versioned_dataset_name, 'dataset_id': dataset_id})

    if find_result:
        return str(find_result['_id'])
    else:
        doc ={
            'dataset_id': dataset_id,
            'bundle_ids': [bundle_id],
            'name': versioned_dataset_name,
            'index': 0,
            'gen_date': None,
            'split': list(dataset_count.as_dict().values()), 
            'preprocessing': [],
            'augmentation': [],
            'status': 0,
            #
            'history': {},
            'ext': {},
            'reg_date': datetime.datetime.utcnow(),
            'reg_id': 'user_id',
            'mod_date': datetime.datetime.utcnow(),
            'mod_id': 'user_id',
        }

        #
        update_result = collection.update_one({'name': versioned_dataset_name}, {'$setOnInsert': doc}, upsert=True)

        #
        return str(update_result.upserted_id)


def update_versioned_dataset(versioned_dataset_id, dataset_count):
    collection = get_collection(_VERSIONED_DATASET_COLLECTION_NAME)
    collection.update_one(
        {'_id': bson.ObjectId(versioned_dataset_id)},
        {'$set': {'split': list(dataset_count.as_dict().values())}}
    )
    return None

