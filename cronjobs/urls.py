from django.conf.urls import url

from . import views
from . import tasks

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^api/execution', views.executions, name='executions'),
    url(r'^api/run', views.run, name='run'),
]
