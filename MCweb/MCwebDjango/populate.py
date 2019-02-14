import unittest
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
        'MCwebDjango.settings')

import django
django.setup()

from django.utils import timezone
from mcwebapp.models import *
from django.contrib.auth.models import User


def populate():
    curr_time = timezone.now()

    # Create superuser.
    # Note: there does not seem to be a "get_or_create" for the superuser, hence the try structure.
    try:
        user = User.objects.get(username='superuser')
        print('Used existing superuser. Are you sure you migrated?')
    except:
        print('Creating superuser...')
        user = User.objects.create_superuser('superuser', 'super@super.com', 'superpass')
        user.save()

    # Create template.
    t = TemplateFile.objects.get_or_create(name='SampleTemplate')[0]
    t.upload_date = curr_time
    t.file_name = 'templateFiles/SampleTemplate.json'
    t.user = user
    t.save()

    # Create PDFFile.
    p = PDFFile.objects.get_or_create(name='PdfFile')[0]
    p.upload_date = curr_time
    p.file_name = 'pdfFiles/SamplePDF.pdf'
    p.template = t
    p.save()

    # Create JSONFile.
    j = JSONFile.objects.get_or_create(name='jsonFile')[0]
    j.upload_date = curr_time
    j.file_name = 'jsonFiles/SamplePDF.json'
    j.pdf = p
    j.save()

    # Create MatchPattern.
    m = MatchPattern.objects.get_or_create(regex='$stuff+(0-9)?')[0]
    m.template = t
    m.save()

if __name__ == '__main__':
    print('Populating the database...')
    populate()
    print('Database population successful.')
