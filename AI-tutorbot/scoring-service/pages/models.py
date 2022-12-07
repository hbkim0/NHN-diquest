from djongo import models


class Page(models.Model):
    _id = models.ObjectIdField()
    workbook_id = models.TextField()
    page_num = models.TextField()
    description = models.TextField()
    original_url = models.TextField()
    sample_url = models.TextField()
    labeled = models.IntegerField()
    width = models.IntegerField()
    height = models.IntegerField()
    vector = models.JSONField()
    problems = models.JSONField()

    # 표준필드
    history = models.JSONField()
    ext = models.JSONField()
    reg_date = models.DateTimeField()
    reg_id = models.TextField()
    mod_date = models.DateTimeField()
    mod_id = models.TextField()

    class Meta:
        ordering = ['-_id', ]
        db_table = "pages"
