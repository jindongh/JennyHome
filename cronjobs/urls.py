from django.conf.urls import url

from . import views
from . import tasks

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^api/workflow/list', views.list_workflow),
    url(r'^api/workflow/update', views.update_workflow),
    url(r'^api/workflow/delete/(?P<id>\d+)', views.delete_workflow),
    url(r'^api/workflow/get/(?P<id>\d+)', views.get_workflow),
    url(r'^api/workflow/run/(?P<id>\d+)', views.run_workflow),
    url(r'^api/workflow/pause/(?P<id>\d+)', views.pause_workflow),
    url(r'^api/workflow/resume/(?P<id>\d+)', views.resume_workflow),
    url(r'^api/workflow/execution', views.executions, name='executions'),
    url(r'^api/step/(?P<stepId>\w+)', views.get_step),
    url(r'^api/test', views.test),
]
