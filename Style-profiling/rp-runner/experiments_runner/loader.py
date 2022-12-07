import pathlib
import pydash as py_
import pandas as pd

from . import database
from . import config

import logging
from typing import Iterable, Mapping, List, Tuple, Callable, Optional
from sklearn.preprocessing import LabelEncoder


class NotSupportedLoader(BaseException):
    pass


class NotSupportedModel(BaseException):
    pass


def _load_data_to_wide_deep(examples: Iterable[Mapping], target_dir: pathlib.Path) -> None:

    #
    target_dir = pathlib.Path(config.FS_BASE_PATH_EXPERIMENTS, target_dir)
    pathlib.Path(target_dir).mkdir(parents=True, exist_ok=True)

    def get_attribute(attributes, key):
        return [ str(sorted(dict_['values'])) for dict_ in attributes if dict_['key'] == key].pop()    

    #
    rows = []

    #
    for example in examples:
        
        product_attributes = py_.get(example, 'product_doc.[0].attributes')

        sample = {
            'customer_id': py_.get(example, 'customer'),
            'product_id': py_.get(example, 'product'),
            'rating': py_.get(example, 'rating'),
            'product_label': py_.get(example, 'product_doc.[0].label'),
            'product_category': get_attribute(product_attributes, '카테고리'),
            'product_length': get_attribute(product_attributes, '기장'),
            'product_style': get_attribute(product_attributes, '스타일'), 
            'product_gender': py_.get(product_attributes,'gender'),
            'product_pattern': get_attribute(product_attributes, '패턴'),
            'product_season': get_attribute(product_attributes, '시즌'),
            'product_fit': get_attribute(product_attributes, '핏'),
            'product_color': get_attribute(product_attributes, '색상'),
            'product_material': get_attribute(product_attributes, '소재'),
            'product_neckline': get_attribute(product_attributes, '넥라인'),        
            'customer_gender': py_.get(example, 'customer_doc.[0].gender'),
            'customer_zipcode': py_.get(example, 'customer_doc.[0].zip_code'),        
        }
        
        rows.append(sample)


    # dataframe
    df = pd.DataFrame(rows)

    for col in list(df.columns):
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])

    df.to_csv(pathlib.Path(target_dir,'input.csv'), index=False)


def _load_data_to_ncf(examples: Iterable[Mapping], target_dir: pathlib.Path)-> None:

    #
    target_dir = pathlib.Path(config.FS_BASE_PATH_EXPERIMENTS, target_dir)
    pathlib.Path(target_dir).mkdir(parents=True, exist_ok=True)

    #
    rows = []

    #
    for example in examples:

        sample = {
            'customer_id': py_.get(example, 'customer'),
            'product_id': py_.get(example, 'product'),
            'rating': py_.get(example, 'rating'),
        }

        rows.append(sample)

    #
    df = pd.DataFrame(rows)
    df.to_csv(pathlib.Path(target_dir,'input.csv'), index=False)


def get_loader_target_dir(experiment: database.Experiment) -> pathlib.Path:
    return pathlib.Path(str(py_.get(experiment,'_id')), 'datasets')


_LOADER_MAP = {
    'Wide and Deep': _load_data_to_wide_deep,
    'Neural Collaborative Filtering': _load_data_to_ncf,
}


def get_loaders(experiment: database.Experiment, target_dir: Optional[pathlib.Path] = None) -> List[Callable]:

    def _factory(func, examples, target_dir):
        return lambda: func(examples, target_dir)

    #
    if target_dir is None:
        target_dir = get_loader_target_dir(experiment)
    
    model = database.get_model(experiment.model_id)

    # model check
    if model is None:
        raise NotSupportedModel(f"not supported model") 

    loader = _LOADER_MAP[model['name']]

    # loader check
    if loader is None:
        raise NotSupportedLoader(f"not supported types: {model['name']}")    

    examples = database.get_data()

    loaders = [
        _factory(loader, examples, target_dir),
    ]

    return loaders
