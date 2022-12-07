import os
import bson
import urllib.parse
import random
import datetime
import traceback
from PIL import Image

from django.core.files.storage import default_storage
from background_task import background

from misc.utils import *
from mlp_data_service.settings import MEDIA_URL, MEDIA_ROOT

from .models import VersionedDataset
from annotations.models import Annotation
from datasets.models import Dataset
from files.models import File
from functions.models import Function

@background()
def generate_versioned_dataset(data):
    dataset_id = data['dataset_id']
    versioned_dataset_id = data['_id']
    versioned_dataset = VersionedDataset.objects.filter(_id=bson.ObjectId(versioned_dataset_id))
    try:
        ml_task = Dataset.objects.get(_id=bson.ObjectId(data['dataset_id'])).ml_task
        annotations = Annotation.objects.filter(dataset_id=data['dataset_id'], bundle_id__in=data['bundle_ids']).exclude(labels=[])

        versioned_dataset.update(status=1)

        prep_functions = []
        aug_functions = []
        if data['preprocessing']:
            prep_functions = list(map(lambda prep: Function.objects.get(_id=bson.ObjectId(prep['function_id'])).function_name,
                                    data['preprocessing']))
        if data['augmentation']:
            aug_functions =list(map(lambda aug: Function.objects.get(_id=bson.ObjectId(aug['function_id'])).function_name, 
                                    data['augmentation']))
        params = [convert_params(data['preprocessing']), convert_params(data['augmentation'])]

        split_roulette = []
        for idx, val in enumerate(versioned_dataset.first().split):
            split_roulette.extend([idx]*val)
        random.shuffle(split_roulette)

        os.makedirs(MEDIA_ROOT+versioned_dataset_id+'/', exist_ok=True)

        for index, annotation in enumerate(annotations):
            file_obj = File.objects.get(_id=bson.ObjectId(annotation.file_id))
            file_name = file_obj.url[len(MEDIA_URL)+len(dataset_id)+2:]

            if ml_task == 0:
                text = default_storage.open(dataset_id+'/'+urllib.parse.unquote(file_name))
                clone_db_docs(file_obj, file_name, annotation, versioned_dataset_id, split_roulette[index], [])
                default_storage.save(versioned_dataset_id+'/'+urllib.parse.unquote(file_name), text)
            else:
                image = Image.open(MEDIA_ROOT+dataset_id+'/'+urllib.parse.unquote(file_name))
                labels = annotation.labels

                if prep_functions:
                    for idx, function in enumerate(prep_functions):
                        image, labels = eval(function)(image, params[0][idx], labels)
                
                if aug_functions and split_roulette[index] == 0:
                    for idx, function in enumerate(aug_functions):
                        aug_image, aug_labels = eval(function)(image, params[1][idx], labels)
                        clone_db_docs(file_obj, function+'_'+file_name, annotation, versioned_dataset_id, 0, aug_labels)
                        aug_image.save(MEDIA_ROOT+versioned_dataset_id+'/'+function+'_'+urllib.parse.unquote(file_name))

                clone_db_docs(file_obj, file_name, annotation, versioned_dataset_id, split_roulette[index], labels)
                image.save(MEDIA_ROOT+versioned_dataset_id+'/'+urllib.parse.unquote(file_name))

        versioned_dataset.update(status=2, gen_date=datetime.datetime.utcnow())
        print('Successfully generated. Annotation='+
            str(Annotation.objects.filter(versioned_dataset_id=versioned_dataset_id).count())+', File='+
            str(File.objects.filter(versioned_dataset_id=versioned_dataset_id).count()))

    except:
        versioned_dataset.update(status=3)
        print(traceback.format_exc())
        print('Generating has been failed.')