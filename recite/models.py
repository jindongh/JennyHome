# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User

from django.db import models

# Create your models here.
class Setting(models.Model):
    user = models.ForeignKey(User)
    key = models.TextField()
    sms = models.TextField(null = True)
    email = models.TextField(null = True)
    mobile = models.TextField(null = True)
    notAfter = models.IntegerField(null = True)
    notBefore = models.IntegerField(null = True)

class Item(models.Model):
    user = models.ForeignKey(User)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

