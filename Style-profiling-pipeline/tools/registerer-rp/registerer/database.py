import datetime
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import logging

from .config import DATABASES


logger = logging.getLogger(__name__)
_mongo_client: MongoClient = None


class ModelDatabase:
    def __init__(self, model: str = None):
        global _mongo_client

        if _mongo_client is None:
            app_name = 'registerer'
            if app_name not in DATABASES:
                raise Exception(f'Not found database configuration for {app_name} : {DATABASES}')

            if 'CLIENT' not in DATABASES[app_name]:
                raise Exception(f'Not found client information for database : {DATABASES[app_name]}')
            client_config = DATABASES[app_name]['CLIENT']

            params = {
                'host': client_config.get('host', ''),
                'port': client_config.get('port', 27017)
            }
            if ('username' in client_config) and ('password' in client_config):
                params['username'] = client_config['username']
                params['password'] = client_config['password']
            client = MongoClient(**params)

            try:
                client.admin.command('ping')
            except ConnectionFailure as e:
                logging.error(f'Server not available(params: {params})')
                raise e
            logger.info(f'server info: ${client.server_info()}')

        self.db_name = "mamihlapinatapai_rp"
        self.db = client[self.db_name]
        self.model = model
        self.col_name = 'models'
        self.problem_type = None

        if self.model == 'Wide and Deep':
            pass
        elif self.model == 'Neural Collaborative Filtering':
            pass
        elif self.model == None:
            print('model type is None: for debug')
        else:
            print('model type error')


    def upsert(self, image_name, **kwargs):
        #
        current_dt = datetime.datetime.utcnow()
        current_user_id = 'registerer'

        doc = {
            "type": self.problem_type,
            "name": f'{self.model}',
            "image_name": image_name,
            "parameters": [
                {'name': 'embedding', 'type': 'integer', 'default': 2},
                {'name': 'lr', 'type': 'double', 'default': 0.001},
                {'name': 'epoch', 'type': 'integer', 'default': 2},
                {'name': 'batch_size', 'type': 'integer', 'default': 16},
            ],
            
            # 표준필드
            'history': {},
            'ext': {},
            'reg_date': current_dt,
            'reg_id': current_user_id,
            'mod_date': current_dt,
            'mod_id': current_user_id,
        }
        if 'cfg_path' in kwargs:
            if kwargs['cfg_path'] != '':
                doc['info']['cfg_path'] = kwargs['cfg_path']

        self.db[self.col_name].update_one({'name': self.model}, {"$set" : doc } , upsert = True)
        return True