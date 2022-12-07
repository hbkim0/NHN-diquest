DATABASES = {
    'experiments_runner': {
        # 'ENGINE': 'pymongo',
        'NAME': 'mamihlapinatapai_rp',
        'CLIENT': {
            'host': '133.186.171.15',
            'port': 27017,
            'username': 'diquest',
            'password': 'ek2znptm2'
        }
    }
}

MEDIA_ROOT = '/ml_data/mamihlapinatapai/origin'
FS_BASE_PATH_FILES = '/ml_data/mamihlapinatapai'
FS_BASE_PATH_EXPERIMENTS = '/ml_data/mamihlapinatapai/experiments'

TRACKING_SERVER_BASE_PATH = '/ml_data/mamihlapinatapai/tracking-server'

LOADER_DIR = {
    'Wide_Deep': 'wide_deep_dataset',
}

RESULT_DIR = {
    'Wide_Deep': 'result_wide_deep',
}


SUPPORT_GPU = False
