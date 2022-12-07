from pymongo import MongoClient
from pymongo.errors import ConnectionFailure


DATABASES = {
    'ingestor': {
        # 'ENGINE': 'pymongo',
        'NAME': 'dataset',
        'CLIENT': {
            'host': 'localhost',
            'port': 27017,
            'username': 'admin',
            'password': 'pass'
        }
    }
}

_mongo_client: MongoClient = None
def _get_mongo_client() -> MongoClient:
    global _mongo_client

    if _mongo_client is None:

        app_name = 'ingestor'
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
            raise e

        _mongo_client = client

    return _mongo_client


def get_db(db: str = "dataset"):
    mongo_client = _get_mongo_client()
    return mongo_client[db]