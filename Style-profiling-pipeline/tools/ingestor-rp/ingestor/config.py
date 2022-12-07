DATABASES = {
    'ingestor': {
        # 'ENGINE': 'pymongo',
        'NAME': 'mamihlapinatapai',
        'CLIENT': {
            'host': '133.186.171.15',
            'port': 27017,
            'username': 'diquest',
            'password': 'ek2znptm2'
        }
    }
}

FS_BASE_PATH = '/style_profiling/mamihlapinatapai/rp-data'

SCHEMA_BASE_PATH = './schemas'
