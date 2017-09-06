from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^api/list', views.get_list, name='list'),
    url(r'^api/add', views.add, name='add'),
    url(r'^api/remove', views.remove, name='remove'),
]
