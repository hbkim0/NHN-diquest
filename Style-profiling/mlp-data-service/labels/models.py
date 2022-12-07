from djongo import models

class Label(models.Model):
    _id = models.ObjectIdField()
    dataset_id = models.TextField()
    name = models.TextField()
    color = models.TextField()

    # 표준필드
    history = models.JSONField()
    ext = models.JSONField()
    reg_date = models.DateTimeField()
    reg_id = models.TextField()
    mod_date = models.DateTimeField()
    mod_id = models.TextField()

    class Meta:
        ordering = ['-_id', ]
        db_table = "labels"

