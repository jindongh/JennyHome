from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', 'garage.views.home', name='home'),
    url(r'^api/state', 'garage.views.state', name='state'),
    url(r'^api/toggle', 'garage.views.toggle', name='toggle'),
)