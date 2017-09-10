from django.db import models

# Create your models here.
class GarageOp(models.Model):
    op_type = models.CharField('Open/Close', max_length=100)
    op_date = models.DateTimeField('Operation Time')
    op_succeed = models.BooleanField('Operation Time', default=False)
    error_message = models.CharField(max_length=1024)

    class Meta:
        permissions = (
                ('check', 'Can see garage status'),
                ('operate', 'Can operate garage'),
                )
    def __str__(self):
        return '%s %s %s' % (self.op_date,
                self.op_type,
                self.op_succeed and 'Succeed' or 'Failed')
