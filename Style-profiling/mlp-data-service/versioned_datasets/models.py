from djongo import models

class VersionedDataset(models.Model):
    _id = models.ObjectIdField()
    dataset_id = models.TextField() 
    bundle_ids =  models.JSONField()
    name = models.TextField()
    index = models.IntegerField() 
    gen_date = models.DateTimeField(null=True)
    split = models.JSONField()
    preprocessing = models.JSONField()
    augmentation = models.JSONField()
    status = models.IntegerField()
    attribute_info = models.JSONField()

    # 표준필드
    history = models.JSONField()
    ext = models.JSONField()
    reg_date = models.DateTimeField()
    reg_id = models.TextField()
    mod_date = models.DateTimeField()
    mod_id = models.TextField()

    class Meta:
        ordering = ['-_id', ]
        db_table = "versioned_datasets" 



    