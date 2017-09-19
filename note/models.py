# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User

from django.db import models

# Create your models here.
class Note(models.Model):
    user = models.ForeignKey(User)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    finished = models.BooleanField(default = False)
    def __str__(self):
        return '%s %s' % (self.date, self.content)
