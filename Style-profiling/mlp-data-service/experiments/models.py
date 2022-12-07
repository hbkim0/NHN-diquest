from djongo import models


class Experiment(models.Model):
    _id = models.ObjectIdField()
    dataset_id = models.TextField()
    versioned_dataset_id = models.TextField()
    model_id = models.TextField()
    name = models.TextField()
    description = models.TextField()
    algorithms = models.JSONField()
    artifacts = models.JSONField()
    status = models.IntegerField()

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