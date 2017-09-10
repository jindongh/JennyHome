from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from . import views
import garage.urls

urlpatterns = [
    # Examples:
    url(r'^$', views.home, name='home'),
    url(r'^garage/', include('garage.urls')),
    url(r'^note/', include('note.urls')),
    url(r'^cronjobs/', include('cronjobs.urls')),

    url('^', include('django.contrib.auth.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/login/$', auth_views.LoginView.as_view(template_name='jennyhome/login.html')),
    url('', include('social_django.urls', namespace='social')),
]
