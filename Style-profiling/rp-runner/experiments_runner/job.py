
import pydash as py_

from .pipeline import Pipeline
from .orchestration import LocalRunner
from . import database
from . import loader
from . import docker
from . import mlflow_api

import logging
from typing import Optional


_logger = logging.getLogger(__name__)
_local_runner: Optional[LocalRunner] = None


def run_experiment():
    global _local_runner

    if _local_runner is not None:
        _logger.info('runner is running...')
        if _local_runner.is_alive():    # 현재 실행 중인 pipeline이 있음.
            return None

        _local_runner = None

    #
    _logger.info('finding an experiment to run...')

    experiment = database.get_experiment()

    if experiment is None:
        return None

    dataset_path = loader.get_loader_target_dir(experiment)

    _logger.info(f'experiment: {experiment}')
    experiment_id = str(experiment._id)

    #
    try:
        _logger.info('creating a pipeline...')

        start_time = lambda: database.update_experiment_time(experiment_id, 'start_time')
        end_time = lambda: database.update_experiment_time(experiment_id, 'end_time')  
        
        loaders = loader.get_loaders(experiment, dataset_path)
        trainers = docker.get_trainers(experiment, dataset_path)
        staging = lambda: mlflow_api.best_model_to_stage()
        
        pipeline = Pipeline(
            name=experiment_id,
            # root='',
            components= [start_time] + loaders + trainers + [staging] + [end_time] 
        )
        _logger.info(f'pipeline: {pipeline}')

    except Exception as e:
        _logger.error(e)
        database.update_experiment_status(experiment_id, database.ExperimentStatus.FAILED)
        return None

    #
    _logger.info('creating runner...')

    database.update_experiment_status(experiment_id, database.ExperimentStatus.TRAINING)
    _local_runner = LocalRunner.run(
        pipeline,
        exception_handler=(lambda: database.update_experiment_status(experiment_id, database.ExperimentStatus.FAILED)),
        done_handler=(lambda: database.update_experiment_status(experiment_id, database.ExperimentStatus.DONE))
    )
