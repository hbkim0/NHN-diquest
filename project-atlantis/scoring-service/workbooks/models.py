from djongo import models


class Workbook(models.Model):
    _id = models.ObjectIdField()
    name = models.TextField()
    description = models.TextField()
    image_url = models.TextField()
    no_pages = models.IntegerField()
    valid = models.IntegerField()
    applied = models.IntegerField()

    # 표준필드
    history = models.JSONField()
    ext = models.JSONField()
    reg_date = models.DateTimeField()
    reg_id = models.TextField()
    mod_date = models.DateTimeField()
    mod_id = models.TextField()

    class Meta:
        ordering = ['-_id', ]
        db_table = "workbooks"
