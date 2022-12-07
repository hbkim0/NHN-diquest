import os

from django.apps import AppConfig

class SchedulesConfig(AppConfig):
    name = 'schedules'

    def ready(self):
        if os.environ.get('RUN_MAIN', None) != 'true':
            from . import tasks
            from background_task.models import Task, CompletedTask

            Task.objects.filter(task_name='schedules.tasks.check_on_time').delete()
            CompletedTask.objects.filter(task_name='schedules.tasks.check_on_time').delete()
            tasks.check_on_time(repeat=60)