import croniter
import datetime
from pytz import timezone

from background_task import background

from .models import Schedule
from experiments.models import Experiment

def duplicate_experiments(schedule):
    for idx, document in enumerate(Experiment.objects.filter(status=0)):
        document._id = None
        document.seq_num_major = schedule.sequence
        document.seq_num_minor = idx+1
        document.status = 1
        document.save()

    schedule.sequence = schedule.sequence+1
    schedule.save()

@background(schedule=60)
def check_on_time():
    try:
        schedule = Schedule.objects.get(priority=1)
    except:
        schedule = None
    
    if schedule:
        now = datetime.datetime.now(timezone('Asia/Seoul'))
        try:
            cron = croniter.croniter(schedule.cron, now)
            next_runtime = cron.get_next(datetime.datetime)
            if abs(next_runtime-now) < datetime.timedelta(minutes=1):
                duplicate_experiments(schedule)
        except Exception as e:
            print(e)




    