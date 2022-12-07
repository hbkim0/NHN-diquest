from djongo import models

class Status(models.Model):
    _id = models.ObjectIdField()
    customer = models.JSONField()
    product = models.JSONField()
    history = models.JSONField()
    date = models.DateField()

    class Meta:
        ordering = ['date', ]
        db_table = "status"

class Customer(models.Model):
    _id = models.ObjectIdField()
    identifier = models.IntegerField()
    gender = models.TextField()
    zip_code = models.IntegerField()
    
    # 표준필드
    history = models.JSONField()
    ext = models.JSONField()
    reg_date = models.DateTimeField()
    reg_id = models.TextField()
    mod_date = models.DateTimeField()
    mod_id = models.TextField()

    class Meta:
        ordering = ['identifier', ]
        db_table = "customers"

class Product(models.Model):
    _id = models.ObjectIdField()
    identifier = models.IntegerField()
    name = models.TextField()
    description = models.TextField()
    image = models.TextField()
    label = models.TextField()
    gender = models.TextField()
    attributes = models.JSONField()
    
    # 표준필드
    history = models.JSONField()
    ext = models.JSONField()
    reg_date = models.DateTimeField()
    reg_id = models.TextField()
    mod_date = models.DateTimeField()
    mod_id = models.TextField()

    class Meta:
        ordering = ['identifier', ]
        db_table = "products"

class History(models.Model):
    _id = models.ObjectIdField()
    customer = models.IntegerField()
    product = models.IntegerField()
    rating = models.IntegerField()
    
    # 표준필드
    history = models.JSONField()
    ext = models.JSONField()
    reg_date = models.DateTimeField()
    reg_id = models.TextField()
    mod_date = models.DateTimeField()
    mod_id = models.TextField()

    class Meta:
        ordering = ['-_id', ]
        db_table = "historys"

