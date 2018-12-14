from django.contrib import admin
from mcwebapp.models import *

admin.site.register(PDFFile)
admin.site.register(JSONFile)
admin.site.register(UserProfile)
admin.site.register(TemplateFile)
admin.site.register(MatchPattern)
# Register your models here.