import dataclasses
import functools
import pathlib
import queue
import pandas as pd
import datetime

import ast
import typer
import yaml
import pydash as py_

from . import main
from . import const
from . import database
from . import utils
from . import config

import logging
from typing import Optional, Tuple


_logger = logging.getLogger(__name__)


def command(dataset_type: const.SupportedDatasetType):
    def wrapper(func):
        @main.app.command(name=dataset_type.value)
        @functools.wraps(func)
        def decorator(*args, **kwargs):
            success_cnt, failed_cnt = func(*args, dataset_type=dataset_type)
            typer.echo(success_cnt)
            typer.echo(failed_cnt)
            return None
        return decorator
    return wrapper


@main.app.command(name='clean')
def clean():

    #
    utils.clean_files()

    #
    for dataset_type in const.SupportedCollection:
        database.get_collection(dataset_type.value).drop()


@command(const.SupportedDatasetType.RECOMMENDATION)
def ingest_data_to_recommendation(
    src_path: str = './dataset/recommend_dataset',
    *, dataset_type: const.SupportedDatasetType = None
):

    #
    src_path = pathlib.Path(src_path)

    #
    typer.echo('searching training dataset...\n', nl=False)

    #
    cols = {
        'customers': ['가입일시', '고객아이디', '성별', '우편번호'],
        'products': ['상품등록일시','품번','상품명','상품이미지','레이블','카테고리','기장','스타일',
                    '성별','패턴', '시즌', '핏', '색상', '소재', '넥라인', '상품정보'],
        'historys':['고객아이디','품번','구매평','구매일시'],
    }

    #
    pathlib.Path(config.FS_BASE_PATH).mkdir(parents=True, exist_ok=True)

    for file in ['customers', 'products', 'historys']:

        failed_cnt = 0
        success_cnt = 0

        #
        columns = cols[file]
        
        #
        file_path = pathlib.Path(src_path, file).with_suffix('.csv')

        #
        df = pd.read_csv(file_path)[columns]

        #
        for idx in range(len(df)):
            
            try: 
                if file == 'customers':
                    doc = {
                        'identifier': int(df.iloc[idx]['고객아이디']),
                        'gender': str(df.iloc[idx]['성별']),
                        'zip_code': int(df.iloc[idx]['우편번호']),
                        'reg_date': datetime.datetime.fromtimestamp(float(df.iloc[idx]['가입일시'])),
                        'mod_date': datetime.datetime.fromtimestamp(float(df.iloc[idx]['가입일시'])),
                    }
                elif file == 'products':
                    doc = {
                        'name': str(df.iloc[idx]['상품명']).rstrip().lstrip(),
                        'description': str(df.iloc[idx]['상품정보']),
                        'image': '/media/' + str(df.iloc[idx]['상품이미지']),
                        'label': str(df.iloc[idx]['레이블']),
                        'identifier': int(df.iloc[idx]['품번']),
                        'gender': str(df.iloc[idx]['성별']),
                        'attributes': [
                            {'key':'카테고리', 'values': ast.literal_eval(df.iloc[idx]['카테고리'])},
                            {'key':'기장', 'values': ast.literal_eval(df.iloc[idx]['기장'])},
                            {'key':'스타일', 'values': ast.literal_eval(df.iloc[idx]['스타일'])},
                            {'key':'패턴', 'values': ast.literal_eval(df.iloc[idx]['패턴'])},
                            {'key':'시즌', 'values': ast.literal_eval(df.iloc[idx]['시즌'])},
                            {'key':'핏', 'values': ast.literal_eval(df.iloc[idx]['핏'])},
                            {'key':'색상', 'values': ast.literal_eval(df.iloc[idx]['색상'])},
                            {'key':'소재', 'values': ast.literal_eval(df.iloc[idx]['소재'])},
                            {'key':'넥라인', 'values': ast.literal_eval(df.iloc[idx]['넥라인'])},
                        ],
                        'reg_date': datetime.datetime.fromtimestamp(float(df.iloc[idx]['상품등록일시'])),
                        'mod_date': datetime.datetime.fromtimestamp(float(df.iloc[idx]['상품등록일시'])),                        
                    }

                    # copy image
                    image_name = str(df.iloc[idx]['상품이미지'])
                    image_path = pathlib.Path(f'{src_path}', 'files', f'{image_name}')

                    dst_path = pathlib.Path(config.FS_BASE_PATH, image_name)
                    
                    dst_path.write_bytes(
                        image_path.read_bytes()
                    )


                elif file == 'historys':
                    doc = {
                        'customer': int(df.iloc[idx]['고객아이디']),
                        'product': int(df.iloc[idx]['품번']),
                        'rating': int(df.iloc[idx]['구매평']),
                        'reg_date': datetime.datetime.fromtimestamp(float(df.iloc[idx]['구매일시'])),
                        'mod_date': datetime.datetime.fromtimestamp(float(df.iloc[idx]['구매일시'])),                          
                    }
                else:
                    failed_cnt +=1

                # 표준필드
                standard_field = {
                    'history': {},
                    'ext': {},
                    'reg_id': 'user_id',
                    'mod_id': 'user_id'
                }
                doc.update(standard_field)
                database.upsert(doc, file)

            except Exception as e:
                _logger.debug(f'failed record {file} with exception: {e}')
                failed_cnt += 1
            else:
                success_cnt += 1
        print(f'{file}: success_cnt: {success_cnt}, failed_cnt : {failed_cnt}')

    return success_cnt, failed_cnt