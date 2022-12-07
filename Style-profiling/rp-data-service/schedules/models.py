from djongo import models

class Schedule(models.Model):
    _id = models.ObjectIdField()
    cron = models.TextField()
    priority = models.IntegerField()
    sequence = models.IntegerField()

    class Meta:
        ordering = ['-_id', ]
        db_table = "schedules"
