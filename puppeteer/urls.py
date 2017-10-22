from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^api/list', views.list_all),
    url(r'^api/get/(?P<codeId>\d+)', views.get),
    url(r'^api/update', views.update),
    url(r'^api/delete/(?P<codeId>\d+)', views.delete),
    url(r'^api/execute', views.execute),
]
