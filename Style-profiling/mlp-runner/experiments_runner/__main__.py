from apscheduler.schedulers.blocking import BlockingScheduler

from .job import run_experiment

import logging

#
logging.basicConfig(
    format='%(asctime)s:%(name)s:%(levelname)s:%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.DEBUG
)

scheduler = BlockingScheduler()
scheduler.add_job(run_experiment, 'interval', seconds=10, id="run_experiment")
scheduler.start()
