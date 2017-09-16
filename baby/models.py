# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User

from django.db import models

# Create your models here.
class Photo(models.Model):
    user = models.ForeignKey(User)
    is_public = models.BooleanField(default = False)
    created = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    image = models.FileField(upload_to='pic_folder/')

class Comment(models.Model):
    photo = models.ForeignKey(Photo)
    user = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
