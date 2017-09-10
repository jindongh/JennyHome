from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^api/state', views.state, name='state'),
    url(r'^api/toggle', views.toggle, name='toggle'),
    url(r'^api/image', views.doorImage, name='image'),
    url(r'^api/cv', views.cvImage, name='cv'),
]
