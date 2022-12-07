import datetime
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import logging
import uuid

from .const import RESOURCE_ID_MODEL
from .config import DATABASES


logger = logging.getLogger(__name__)
_mongo_client: MongoClient = None


class AlgorithmDatabase:
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

        self.db_name = "mamihlapinatapai"
        self.db = client[self.db_name]
        self.model = model
        self.col_name = 'algorithms'
        self.problem_type = None

        if self.model == 'Yolov5':
            self.problem_type = 11      # image object detection
        elif self.model == 'Classifier(resnet50)':
            self.problem_type = 13      # image classification (multi-label)
        elif self.model == 'Classifier(resnet101)':
            self.problem_type = 13      # image classification (multi-label)
        elif self.model == 'Koelectra(base)':
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