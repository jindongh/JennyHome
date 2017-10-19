from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^access/(?P<bookmarkId>\d+)', views.access_bookmark),
    url(r'^api/category/(?P<categoryId>-?\d+)', views.list_bookmark),
    url(r'^api/category/edit', views.edit_category),
    url(r'^api/category/delete/(?P<categoryId>\d+)', views.delete_category),
    url(r'^api/bookmark/edit/(?P<categoryId>\d+)', views.edit_bookmark),
    url(r'^api/bookmark/delete/(?P<bookmarkId>\d+)', views.delete_bookmark),
]
