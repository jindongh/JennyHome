from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^api/history', views.history),
    url(r'^api/name', views.setName),

    url(r'^api/relay', views.relay),
    url(r'^api/display', views.display),
    url(r'^api/temperature', views.temperature),
]
