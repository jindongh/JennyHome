from django.conf.urls import include, url
from django.contrib import admin

from . import views
import garage.urls

urlpatterns = [
    # Examples:
    url(r'^$', views.home, name='home'),
    url(r'^garage/', include('garage.urls')),

    url(r'^admin/', admin.site.urls),
]
