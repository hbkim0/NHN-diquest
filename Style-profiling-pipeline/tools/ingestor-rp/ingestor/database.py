import collections
import dataclasses
import datetime
import bson

import pymongo
import pymongo.collection
import pymongo.errors

from . import const
from . import config
from . import utils

import logging


_DATABASE_NAME = 'mamihlapinatapai_rp'


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



def upsert(doc, file):
    collection = get_collection(f'{file}')

    if file in ['customers', 'products']:
        update_result = collection.update_one({'identifier': doc['identifier']}, {'$setOnInsert': doc}, upsert=True)
    elif file == 'historys':
        update_result = collection.update_one({'customer': doc['customer'], 'product': doc['product']}, {'$setOnInsert': doc}, upsert=True)
    else:
        update_result = None

    return update_result.upserted_id is not None
    

