from django.db import models

# Create your models here.
class GarageOp(models.Model):
    op_type = models.CharField('Open/Close', max_length=100)
    op_date = models.DateTimeField('Operation Time')
    op_succeed = models.BooleanField('Operation Time', default=False)
    error_message = models.CharField(max_length=1024)

