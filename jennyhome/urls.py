from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'jennyhome.views.home', name='home'),
    url(r'^garage/', include('garage.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
