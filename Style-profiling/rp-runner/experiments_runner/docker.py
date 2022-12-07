import collections
import pathlib
import os

import pydash as py_
import docker


from . import config
from . import database

import logging
from typing import Mapping, List, Callable

class NotSupportedTrainer(BaseException):
    pass


class NotSupportedPusher(BaseException):
    pass


_logger = logging.getLogger(__name__)

def _wide_deep_run(_id, image_name, loader_dir, epoch, batch_size, lr, embedding_dim):

    #
    loader_dir = pathlib.Path(config.FS_BASE_PATH_EXPERIMENTS, loader_dir).resolve()

    #
    tracking_server_dir = pathlib.Path(config.TRACKING_SERVER_BASE_PATH)

    #
    result_dir = pathlib.Path(config.FS_BASE_PATH_EXPERIMENTS, _id)
    result_dir.mkdir(parents=True, exist_ok=True)

    client = docker.from_env()

    volumes = [
        f'{str(tracking_server_dir)}:/usr/src/app/tracking-server', 
        f'{str(loader_dir)}:/usr/src/datasets',
        f'{str(result_dir)}:/usr/src/app/exp_results',
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
            '--data ../datasets/input.csv',
            '--tensorboard-logdir exp_results',
            f'--epochs {epoch}',
            f'--batch-size {batch_size}',
            f'--n-embedding {embedding_dim}',
            f'--learning-rate {lr}',
            f'--exp-id {_id}'
        ])
    ]    

    client.containers.run(image = image_name, device_requests = device_requests,
                        command = ' '.join(cli_command), 
                        volumes = volumes, ipc_mode = 'host',
                        stdin_open = True, tty = True, remove = True, detach = False)  


def _ncf_run(_id, image_name, loader_dir, epoch, batch_size, lr, embedding_dim):

    #
    loader_dir = pathlib.Path(config.FS_BASE_PATH_EXPERIMENTS, loader_dir).resolve()

    #
    tracking_server_dir = pathlib.Path(config.TRACKING_SERVER_BASE_PATH)

    #
    result_dir = pathlib.Path(config.FS_BASE_PATH_EXPERIMENTS, _id)
    result_dir.mkdir(parents=True, exist_ok=True)

    client = docker.from_env()

    volumes = [
        f'{str(tracking_server_dir)}:/usr/src/app/tracking-server', 
        f'{str(loader_dir)}:/usr/src/datasets',
        f'{str(result_dir)}:/usr/src/app/exp_results',
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
            '--data ../datasets/input.csv',
            '--tensorboard-logdir exp_results',
            f'--epochs {epoch}',
            f'--batch-size {batch_size}',
            f'--n-embedding {embedding_dim}',
            f'--learning-rate {lr}',
            f'--exp-id {_id}'
        ])
    ]

    #
    client.containers.run(image = image_name, device_requests = device_requests,
                        command = ' '.join(cli_command), 
                        volumes = volumes, ipc_mode = 'host',
                        stdin_open = True, tty = True, remove = True, detach = False)  
    


_TRAINER_MAP={
    'Wide and Deep': _wide_deep_run,
    'Neural Collaborative Filtering': _ncf_run,
}


def get_trainers(experiment: database.Experiment, dataset_dir: pathlib.Path) -> List[Callable]:

    def _factory(func, _id, image_name, loader_dir, **kwarg):
        return lambda: func(_id, image_name, loader_dir, **kwarg)

    def update_metric(experiment_id):
        return lambda: database.update_experiment_metric(experiment_id)  

    model = database.get_model(experiment.model_id)
    
    parameters = {}
    for param in experiment.parameters:
        parameters[param['key']] = param['value']

    trainer = _TRAINER_MAP[model['name']]
    if trainer is None:
        raise NotSupportedTrainer(f"not supported trainer: {model['name']}")
    
    #
    trainers = [
        _factory(
            trainer,
            str(experiment._id),
            model['image_name'],
            str(dataset_dir),
            **parameters
        ),
        update_metric(str(experiment._id)),
    ]

    return trainers