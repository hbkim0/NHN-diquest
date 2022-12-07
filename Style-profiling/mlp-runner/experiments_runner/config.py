DATABASES = {
    'experiments_runner': {
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

MEDIA_ROOT = '/style_profiling/mamihlapinatapai'

FS_BASE_PATH_EXPERIMENTS = '/style_profiling/mamihlapinatapai/experiments'

TRACKING_SERVER_BASE_PATH = '/style_profiling/mamihlapinatapai/tracking-server'

LOADER_DIR = {
    'Yolov5(small)': 'yolov5_dataset',
    'Yolov5(medium)': 'yolov5_dataset',
    'Koelectra(base)':'koelectra_dataset',
    'Classifier(resnet50)': 'classifier_dataset',
    'Classifier(resnet101)': 'classifier_dataset',
}

RESULT_DIR = {
    'Yolov5(small)': 'result_yolov5',
    'Yolov5(medium)': 'result_yolov5',
    'Koelectra(base)':'result_koelectra',
    'Classifier(resnet50)': 'result_classifier',
    'Classifier(resnet101)': 'result_classifier',
}


SUPPORT_GPU = False
