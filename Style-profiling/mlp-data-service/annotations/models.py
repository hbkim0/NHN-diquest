from djongo import models


class Annotation(models.Model):
    _id = models.ObjectIdField()
    dataset_id = models.TextField()
    bundle_id = models.TextField()
    file_id = models.TextField()
    versioned_dataset_id = models.TextField()
    description = models.TextField()
    done = models.IntegerField()
    split = models.IntegerField(blank=True, null=True)
    labels = models.JSONField()

    # 표준필드
    history = models.JSONField()
    ext = models.JSONField()
    reg_date = models.DateTimeField()
    reg_id = models.TextField()
    mod_date = models.DateTimeField()
    mod_id = models.TextField()

    class Meta:
        ordering = ['-_id', ]
        db_table = "annotations"