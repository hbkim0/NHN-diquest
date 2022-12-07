import urllib.parse
import datetime
from PIL import Image, ImageFilter

from mlp_data_service.settings import MEDIA_URL

def convert_params(params_list):
    result = []
    for obj in params_list:
        result.append({ x.get('name'): x.get('value', None) for x in obj.get('params', [])})

    return result

def clone_db_docs(file_obj, file_name, annotation_obj, versioned_dataset_id, split, labels):
    current_dt = datetime.datetime.utcnow()
    patch_data = {
        '_id': None,
        'dataset_id': '',
        'versioned_dataset_id': versioned_dataset_id,
        'name': urllib.parse.unquote(file_name),
        'url': '/'+MEDIA_URL+versioned_dataset_id+'/'+file_name,
        'reg_date': current_dt,
        'mod_date': current_dt,
    }

    file_obj.__dict__.update(patch_data)
    file_obj.save()

    patch_data.pop('name')
    patch_data.pop('url')
    patch_data['file_id'] = str(file_obj._id)
    patch_data['split'] = split
    if labels:
        patch_data['labels'] = labels

    annotation_obj.__dict__.update(patch_data)
    annotation_obj.save()

def resize_img(image, params, labels):
    o_width, o_height = image.size
    width = int(params.get('Width', o_width))
    height = int(params.get('Height', o_height))
    image = image.resize((width, height))

    for label in labels:
        label['bbox'] = [
            label['bbox'][0]*width/o_width,
            label['bbox'][1]*height/o_height,
            label['bbox'][2]*width/o_width,
            label['bbox'][3]*height/o_height
        ]

    return image, labels

def grayscale_img(image, params, labels):
    image = image.convert("L")

    return image, labels

def flip_img(image, params, labels):
    width, height = image.size
    horizontal = params.get('Horizontal', False)
    vertical = params.get('Vertical', False)

    if horizontal:
        image = image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        for label in labels:
            label['bbox'] = [
                width-label['bbox'][2],
                label['bbox'][1],
                width-label['bbox'][0],
                label['bbox'][3]
            ]
    if vertical:
        image = image.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        for label in labels:
            label['bbox'] = [
                label['bbox'][0],
                height-label['bbox'][3],
                label['bbox'][2],
                height-label['bbox'][1]
            ]

    return image, labels

def rotate_img(image, params, labels):
    width, height = image.size
    rotate_90 = params.get('90°', False)
    rotate_180 = params.get('180°', False)
    rotate_270 = params.get('270°', False)

    if rotate_90:
        image = image.transpose(Image.Transpose.ROTATE_90).resize((width, height))
        for label in labels:
            label['bbox'] = [
                height-label['bbox'][1],
                label['bbox'][2],
                height-label['bbox'][3],
                label['bbox'][0]
            ]
    if rotate_180:
        image = image.transpose(Image.Transpose.ROTATE_180)
        for label in labels:
            label['bbox'] = [
                height-label['bbox'][1],
                label['bbox'][2],
                height-label['bbox'][3],
                label['bbox'][0]
            ]     
    if rotate_270:
        image = image.transpose(Image.Transpose.ROTATE_270).resize((width, height))
        for label in labels:
            label['bbox'] = [
                label['bbox'][3],
                width-label['bbox'][0],
                label['bbox'][1],
                width-label['bbox'][2]
            ]

    return image, labels

def blur_img(image, params, labels):
    image = image.filter(ImageFilter.BLUR)

    return image, labels