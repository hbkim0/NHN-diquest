from apscheduler.schedulers.blocking import BlockingScheduler

from .job import run_experiment
from . import database

import logging

logging.basicConfig(
    format='%(asctime)s:%(name)s:%(levelname)s:%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.DEBUG
)

scheduler = BlockingScheduler(timezone='Asia/Seoul')
scheduler.add_job(run_experiment, 'interval', seconds=10, id = 'run_experiment')
scheduler.start()









