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

FS_BASE_PATH_EXPERIMENTS = '/style_profiling/mamihlapinatapai/experiments'

TRACKING_SERVER_BASE_PATH = '/style_profiling/mamihlapinatapai/tracking-server'

SUPPORT_GPU = False
