
DATABASES = {
    'registerer': {
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



WIDE_DEEP = {
    'base_path': {
        'dockerfile': 'wide-deep-model/',
    },
}

NCF = {
    'base_path': {
        'dockerfile': 'neural-collaborative-filtering/',
    },
}