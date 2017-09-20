from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^gallery/(?P<galleryId>\d)', views.showGallery, name='gallery'),
    url(r'^addGallery', views.addGallery, name='addGallery'),
    url(r'^api/list/(?P<galleryId>\d)', views.listPhotos, name='list'),
    url(r'^api/upload/(?P<galleryId>\d)', views.uploadPhoto, name='upload'),
    url(r'^api/delete/(?P<photoId>\d+)', views.deletePhoto, name='delete'),
    url(r'^api/image/(?P<photoId>\d+)', views.getImage, name='image'),
]
