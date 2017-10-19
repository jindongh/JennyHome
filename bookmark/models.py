# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User

from django.db import models

# Create your models here.
class Category(models.Model):
    user = models.ForeignKey(User)
    name = models.TextField()

class Bookmark(models.Model):
    user = models.ForeignKey(User)
    category = models.ForeignKey(Category)
    name = models.TextField()
    link = models.TextField()
    click = models.IntegerField(default = 0)
