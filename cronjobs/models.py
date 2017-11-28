# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

from puppeteer.models import Script

class Step(models.Model):
    user = models.ForeignKey(User, null=True)
    name = models.CharField(max_length=256)
    type = models.CharField(max_length=266)
    data = models.TextField()

# Create your models here.
class Workflow(models.Model):
    user = models.ForeignKey(User, null=True)
    name = models.CharField(max_length=256)
    data = models.TextField()

class Execution(models.Model):
    workflow = models.ForeignKey(Workflow)
    data = models.TextField()
