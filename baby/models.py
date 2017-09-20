# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User

from django.db import models

# Create your models here.
class Gallery(models.Model):
    name = models.CharField(max_length=1024)
    user = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    is_public = models.BooleanField(default = False)

class Photo(models.Model):
    gallery = models.ForeignKey(Gallery)
    created = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    image = models.FileField(upload_to='pic_folder/')

class Comment(models.Model):
    photo = models.ForeignKey(Photo)
    user = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
