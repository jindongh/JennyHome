# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User

from django.db import models

# Create your models here.
class Blog(models.Model):
    user = models.ForeignKey(User)
    title = models.TextField()
    tags = models.TextField()
    content = models.TextField()
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)
    publish = models.BooleanField(default = False)
    def tags_as_list(self):
        return self.tags.split(',')
    def __str__(self):
        return '%s %s' % (self.user, self.title)

class Tag(models.Model):
    user = models.ForeignKey(User)
    name = models.TextField()
