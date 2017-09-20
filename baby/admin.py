# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Gallery
from .models import Photo
from .models import Comment

# Register your models here.
admin.site.register(Gallery)
admin.site.register(Photo)
admin.site.register(Comment)
