from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(r'^garage/', include('garage.urls')),
    url(r'^note/', include('note.urls')),
    url(r'^baby/', include('baby.urls')),
    url(r'^cronjobs/', include('cronjobs.urls')),
    url(r'^bookmark/', include('bookmark.urls')),
    url(r'^puppeteer/', include('puppeteer.urls')),
    url(r'^iot/', include('iot.urls')),
    url(r'^recite/', include('recite.urls')),

    url(r'^$', views.blog, name='home'),
    url('^blog/blog', views.blog, name='blog'),
    url('^blog/delblog', views.del_blog, name='delblog'),
    url('^blog/prepare', views.prepare_blog, name='prepare'),
    url('^blog/tag', views.tag, name='tag'),
    url('^blog/deltag', views.del_tag, name='deltag'),

    url('^', include('django.contrib.auth.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/login/$', auth_views.LoginView.as_view(template_name='jennyhome/login.html')),
    url('', include('social_django.urls', namespace='social')),
]
