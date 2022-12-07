from djongo import models

class Experiment(models.Model):
    _id = models.ObjectIdField()
    model_id = models.TextField()
    seq_num_major = models.IntegerField()
    seq_num_minor = models.IntegerField()
    status = models.IntegerField()
    serving = models.IntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    parameters = models.JSONField()
    rmse = models.FloatField()

    # 표준필드
    history = models.JSONField()
    ext = models.JSONField()
    reg_date = models.DateTimeField()
    reg_id = models.TextField()
    mod_date = models.DateTimeField()
    mod_id = models.TextField()

    class Meta:
        ordering = ['-_id', ]
        db_table = "experiments"