# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User

from django.db import models

# Create your models here.
class Script(models.Model):
    user = models.ForeignKey(User, null=True)
    name = models.TextField()
    code = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
