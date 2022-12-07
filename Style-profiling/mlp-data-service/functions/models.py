from djongo import models


class Function(models.Model):
    _id = models.ObjectIdField()
    ml_task = models.IntegerField()
    type = models.IntegerField()
    name = models.TextField()
    params = models.JSONField()
    function_name = models.TextField()

    # 표준필드
    history = models.JSONField()
    ext = models.JSONField()
    reg_date = models.DateTimeField()
    reg_id = models.TextField()
    mod_date = models.DateTimeField()
    mod_id = models.TextField()

    class Meta:
        ordering = ['-_id', ]
        db_table = "functions"