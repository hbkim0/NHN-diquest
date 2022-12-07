from djongo import models


class Log(models.Model):
    _id = models.ObjectIdField()
    success = models.IntegerField()
    workbook = models.JSONField(default={})
    page = models.JSONField(default={})
    input_url = models.TextField()
    boxed_url = models.TextField(default='')
    scoring = models.JSONField(default=[])
    user_id = models.TextField()

    # 표준필드
    reg_date = models.DateTimeField()
    reg_id = models.TextField()

    class Meta:
        ordering = ['-_id', ]
        db_table = "logs"
