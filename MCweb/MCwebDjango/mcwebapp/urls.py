from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from registration.backends.simple.views import RegistrationView

from django.conf.urls import url

from django.conf.urls import include
from . import views
from django.contrib.auth import logout


urlpatterns = [
        path('', views.index, name='index'),
        #url(r'^register/$', views.register, name='register'),
        ]
