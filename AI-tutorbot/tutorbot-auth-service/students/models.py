from djongo import models

class Student(models.Model):
    _id = models.ObjectIdField()
    name = models.TextField()
    user_id = models.TextField()
    workbook_id = models.TextField()
    correct_rate = models.IntegerField()
    correct_count = models.IntegerField()
    correct_count_all = models.IntegerField()
    page_done = models.IntegerField()
    pages_today = models.JSONField()
    pages_tomorrow = models.JSONField()
    person_type = models.TextField()

    # 표준필드
    history = models.JSONField()
    ext = models.JSONField()
    reg_date = models.DateTimeField()
    reg_id = models.TextField()
    mod_date = models.DateTimeField()
    mod_id = models.TextField()

    class Meta:
        ordering = ['-_id', ]
        db_table = "students"