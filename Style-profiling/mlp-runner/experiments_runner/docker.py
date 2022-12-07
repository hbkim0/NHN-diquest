import collections
import pathlib
import os

import pydash as py_
import docker


from . import const
from . import config
from . import database

import logging
from typing import Mapping, List, Callable


class NotSupportedTrainer(BaseException):
    pass


class NotSupportedPusher(BaseException):
    pass


_logger = logging.getLogger(__name__)


def _yolov5s_run(_id, image_name, loader_dir, result_dir, epoch, batch_size, workers = 1):

    # input
    loader_dir = pathlib.Path(config.FS_BASE_PATH_EXPERIMENTS, loader_dir).resolve()

    # output
    result_base_dir = pathlib.Path(config.FS_BASE_PATH_EXPERIMENTS, str(_id), result_dir).resolve()
    result_base_dir.mkdir(parents=True, exist_ok=True)

    #
    tracking_server_dir = pathlib.Path(config.TRACKING_SERVER_BASE_PATH)

    # 
    client = docker.from_env()

    #
    volumes = [
        f'{str(tracking_server_dir)}:/usr/src/app/tracking-server', 
        f'{str(loader_dir)}:/usr/src/datasets',
        f'{str(result_base_dir)}:/usr/src/app/exp_results',
    ]

    #
    if config.SUPPORT_GPU:
        device_requests = [docker.types.DeviceRequest(count=-1, capabilities=[['gpu']])]
    else:
        device_requests = None

    #
    cli_command = [
        ' '.join([
            'python train.py',
            '--cfg models/yolov5s.yaml',
            '--data ../datasets/dataset.yaml',
            '--project exp_results',
            '--name results',
            f'--epochs {epoch}',
            f'--batch-size {batch_size}',
            f'--workers {workers}',
            '--exist-ok'
        ])
    ]

    client.containers.run(image = image_name, device_requests = device_requests,
                        command = ' '.join(cli_command), 
                        volumes = volumes, ipc_mode = 'host',
                        stdin_open = True, tty = True, remove = True, detach = False)   


def _yolov5m_run(_id, image_name, loader_dir, result_dir, epoch, batch_size, workers = 1):

    # input
    loader_dir = pathlib.Path(config.FS_BASE_PATH_EXPERIMENTS, loader_dir).resolve()

    # output
    result_base_dir = pathlib.Path(config.FS_BASE_PATH_EXPERIMENTS, str(_id), result_dir).resolve()
    result_base_dir.mkdir(parents=True, exist_ok=True)

    #
    tracking_server_dir = pathlib.Path(config.TRACKING_SERVER_BASE_PATH)

    # 
    client = docker.from_env()

    #
    volumes = [
        f'{str(tracking_server_dir)}:/usr/src/app/tracking-server', 
        f'{str(loader_dir)}:/usr/src/datasets',
        f'{str(result_base_dir)}:/usr/src/app/exp_results',
    ]

    #
    if config.SUPPORT_GPU:
        device_requests = [docker.types.DeviceRequest(count=-1, capabilities=[['gpu']])]
    else:
        device_requests = None

    #
    cli_command = [
        ' '.join([
            'python train.py',
            '--cfg models/yolov5m.yaml',
            '--data ../datasets/dataset.yaml',
            '--project exp_results',
            '--name results',
            f'--epochs {epoch}',
            f'--batch-size {batch_size}',
            f'--workers {workers}',
            '--exist-ok'
        ])
    ]

    client.containers.run(image = image_name, device_requests = device_requests,
                        command = ' '.join(cli_command), 
                        volumes = volumes, ipc_mode = 'host',
                        stdin_open = True, tty = True, remove = True, detach = False)   


def _image_tagging_classifier_run(_id, image_name, loader_dir, result_dir, epoch, batch_size):

    # input
    loader_dir = pathlib.Path(config.FS_BASE_PATH_EXPERIMENTS, loader_dir).resolve()

    # output
    result_base_dir = pathlib.Path(config.FS_BASE_PATH_EXPERIMENTS, str(_id), result_dir).resolve()
    result_base_dir.mkdir(parents=True, exist_ok=True)

    #
    tracking_server_dir = pathlib.Path(config.TRACKING_SERVER_BASE_PATH)

    # 
    client = docker.from_env()

    #
    volumes = [
        f'{str(tracking_server_dir)}:/usr/src/app/tracking-server', 
        f'{str(loader_dir)}:/usr/src/datasets',
        f'{str(result_base_dir)}:/usr/src/app/exp_results',
    ]

    #
    if config.SUPPORT_GPU:
        device_requests = [docker.types.DeviceRequest(count=-1, capabilities=[['gpu']])]
    else:
        device_requests = None

    # classifier 
    cli_command = [
        ' '.join([
            'python train.py',
            '--data ../datasets',
            f'--output-path exp_results',
            f'--epochs {epoch}',
            f'--batch-size {batch_size}',
            f'--device cuda' if config.SUPPORT_GPU else '',
        ])
    ]    

    client.containers.run(image = image_name, device_requests = device_requests,
                        command = ' '.join(cli_command), 
                        volumes = volumes, ipc_mode = 'host',
                        stdin_open = True, tty = True, remove = True, detach = False) 


def _koelectra_base_run(_id, image_name, loader_dir, result_dir, epoch, batch_size):

    # input
    loader_dir = pathlib.Path(config.FS_BASE_PATH_EXPERIMENTS, loader_dir).resolve()

    # output
    result_base_dir = pathlib.Path(config.FS_BASE_PATH_EXPERIMENTS, str(_id), result_dir).resolve()
    result_base_dir.mkdir(parents=True, exist_ok=True)

    #
    tracking_server_dir = pathlib.Path(config.TRACKING_SERVER_BASE_PATH)

    # 
    client = docker.from_env()

    #
    volumes = [
        f'{str(tracking_server_dir)}:/usr/src/app/tracking-server', 
        f'{str(loader_dir)}:/usr/src/datasets',
        f'{str(result_base_dir)}:/usr/src/app/exp_results',
    ]

    #
    if config.SUPPORT_GPU:
        device_requests = [docker.types.DeviceRequest(count=-1, capabilities=[['gpu']])]
    else:
        device_requests = None

    cli_command = [
        ' '.join([
            'python train.py',
            f'--epochs {epoch}',
            f'--batch-size {batch_size}',            
        ])
    ]

    client.containers.run(image = image_name, device_requests = device_requests,
                        command = ' '.join(cli_command), 
                        volumes = volumes, ipc_mode = 'host',
                        stdin_open = True, tty = True, remove = True, detach = False) 


_TRAINER_MAP={
    'Yolov5(small)': _yolov5s_run,
    'Yolov5(medium)': _yolov5m_run,
    'Classifier(resnet50)': _image_tagging_classifier_run,
    'Classifier(resnet101)': _image_tagging_classifier_run,
    'Koelectra(base)': _koelectra_base_run,
}


def get_trainers(experiment: database.Experiment, dataset_dir_root: pathlib.Path) -> List[Callable]:

    def _factory(func, _id, image_name, loader_dir, result_dir, **kwarg):
        return lambda: func(_id, image_name, loader_dir, result_dir, **kwarg)

    def update_status(experiment, name, result_dir):
        exp_id = str(experiment._id)
        tensorboard_logdir = pathlib.Path(exp_id, result_dir)
        return lambda: database.update_experiment_artifacts(exp_id, name, 'tensorboard_logdir', str(tensorboard_logdir))

    #
    model_id = py_.get(experiment, 'model_id')
    models = database.get_models(model_id)

    # 
    algorithms = py_.get(experiment, 'algorithms')

    trainers = []
    for algorithm in algorithms:

        #
        ls_params = algorithm['training_params']
        hyper_params = {}
        for params in ls_params:
            hyper_params[params['name']] = params['argument']

        #
        name = algorithm['name']
        func = _TRAINER_MAP[name]
        image_name = [ algo['image_name'] for algo in py_.get(models, 'algorithms') if algo['name'] == name].pop()

        #
        dataset_dir = pathlib.Path(dataset_dir_root, config.LOADER_DIR[name])
        result_dir = config.RESULT_DIR[name]

        #
        trainers.append(_factory(func, experiment._id, image_name, dataset_dir, result_dir, **hyper_params))
        trainers.append(update_status(experiment, name, result_dir))

    return trainers
