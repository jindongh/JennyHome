# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Thing(models.Model):
    id = models.CharField(max_length = 256, primary_key=True)
    name = models.CharField(max_length = 256)
    state = models.CharField(max_length = 256)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now = True)

class Operation(models.Model):
    thing = models.ForeignKey(Thing)
    created = models.DateTimeField(auto_now_add=True)
    event = models.CharField(max_length = 256)

