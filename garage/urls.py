from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^api/state', views.state, name='state'),
    url(r'^api/toggle', views.toggle, name='toggle'),
]
