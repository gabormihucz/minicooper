from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from registration.backends.simple.views import RegistrationView

from django.conf.urls import include
from django.contrib.auth import logout


urlpatterns = [
        path('', views.index, name=''),
        path('upload_pdf/', views.upload_pdf, name='uploadPDF'),
        path('get_pdf_info/', views.get_pdf_info, name='getPDFInfo'),
        path('save_template/', views.save_template, name='saveTemplate'),
        path('search_files/', views.search, name='search'),
        path('template_manager/', views.manage_templates,name='templateManager'),
        path('search_templates/', views.search_templates, name='searchTemplates')
        ]
