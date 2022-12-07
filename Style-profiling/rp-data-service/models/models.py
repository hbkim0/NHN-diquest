from djongo import models

class Model(models.Model):
    _id = models.ObjectIdField()
    name = models.TextField()
    description = models.TextField()
    image_name = models.TextField()
    parameters = models.JSONField()

    # 표준필드
    history = models.JSONField()
    ext = models.JSONField()
    reg_date = models.DateTimeField()
    reg_id = models.TextField()
    mod_date = models.DateTimeField()
    mod_id = models.TextField()

    class Meta:
        ordering = ['-_id', ]
        db_table = "models"