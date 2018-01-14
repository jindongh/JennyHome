from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^history', views.history),
    url(r'^setting', views.setting),
    url(r'^add', views.add),
    url(r'^delete', views.delete),
]
