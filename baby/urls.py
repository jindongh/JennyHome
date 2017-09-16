from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^api/list', views.listPhotos, name='list'),
    url(r'^api/image/(?P<photoId>\d+)', views.getImage, name='image'),
    url(r'^api/upload', views.uploadPhoto, name='upload'),
]
