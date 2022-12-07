
DATABASES = {
    'registerer': {
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

Yolov5 = {
    'default_path': {
        'dockerfile': 'yolov5/',
        'cfg_path': '',
    }
}



IMAGE_TAGGING_CLASSIFIER = {
    'resnet50_path': {
        'dockerfile': 'image-tagging-classifier-resnet50/',
    },
    'resnet101_path': {
        'dockerfile': 'image-tagging-classifier-resnet101/',
    },
}

KOELECTRA = {
    'base_path': {
        'dockerfile': 'koelectra-base/',
    },
}