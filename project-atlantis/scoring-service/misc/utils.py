import base64
import requests
import numpy as np
import cv2

from scoring_service.settings import SEARCH_MODEL_URL, RECOGNITION_MODEL_URL


_BASE64_HEADER = 'data:image/' + '.jpg' +';base64'


def get_resized_shape(width, height, threshold=1000):
    resize_ratio = 1
    while (width/resize_ratio) >= threshold and (height/resize_ratio) >= threshold:
        resize_ratio += 1

    new_width = int(width/resize_ratio)
    new_height = int(height/resize_ratio)
    return new_width, new_height


def _convert_item(item):
    if isinstance(item, np.ndarray):
        item = cv2.imencode('.jpg', item)[1].tostring()
    elif isinstance(item, bytes):
        pass
    else:
        return None

    base64_item = base64.encodebytes(item).decode('utf8')
    
    return _BASE64_HEADER + base64_item


class SearchModel():
    def __init__(self):
        self.model = SEARCH_MODEL_URL
        self.version = '1.0.0'

    def __call__(self, input):
        if isinstance(input, dict):
            single_input = False
            model_input = dict()
            for key in input:
                model_input[key] = _convert_item(input[key])
        else:
            single_input = True
            model_input = {'input': _convert_item(input)}
        
        model_output = requests.post(self.model, model_input)

        output = model_output.json()
        if single_input:
            output = output.get('input')

        return output
    
    def get_version(self):
        return self.version


class RecognitionModel():
    def __init__(self):
        self.model = RECOGNITION_MODEL_URL
        self.version = '1.0.0'

    def __call__(self, input):
        if isinstance(input, list):
            model_input = dict()
            for cnt, item in enumerate(input):
                model_input[str(cnt)] = _convert_item(item)
        else:
            return None
        
        model_output = requests.post(self.model, model_input)

        output = model_output.json()
        output = list(output.values())

        return output

    def get_version(self):
        return self.version