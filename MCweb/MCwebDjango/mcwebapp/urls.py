from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from registration.backends.simple.views import RegistrationView

from django.conf.urls import include
from django.contrib.auth import logout

# Create a new class that redirects the user to the index page,
#if successful at logging

class MyRegistrationView(RegistrationView):
    def get_success_url(self, user):
        return ''

urlpatterns = [
        path('', views.index, name=''),
        path('upload_pdf/', views.upload_pdf, name='uploadPDF'),
        path('save_template/', views.save_template, name='saveTemplate'),
        path('search_files/', views.search, name='search'),
        path('template_manager/<int:temp_id>', views.manage_templates,name='templateManager'),
        path('template_manager/', views.manage_templates,name='templateManager'),
        path('search_templates/', views.search_templates, name='searchTemplates'),
        path('accounts/', include('registration.backends.simple.urls')),
	    path('accounts/register/',MyRegistrationView.as_view(),name='registration_register'),
	    path('template_creator/',views.template_creator,name='template_creator'),
        path('template_editor/<str:temp_name>',views.template_editor,name='template_editor'),
	    path('search_files/', views.search, name='search_files'),
        path('json/<slug:json_slug>/', views.json_popup, name='json_popup'),
	    path('get_more_tables/', views.get_more_tables, name='get_more_tables'),
        ]
