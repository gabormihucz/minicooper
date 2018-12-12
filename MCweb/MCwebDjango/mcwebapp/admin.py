from django.contrib import admin
from mcwebapp.models import UserProfile
from mcwebapp.models import PdfFile

admin.site.register(PdfFile)

admin.site.register(UserProfile)


# Register your models here.
