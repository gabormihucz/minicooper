from django.db import models

class PdfFile(models.Model):
    file_name = models.CharField(max_length = 200)
    upload_date = models.DateTimeField('date uploaded')
