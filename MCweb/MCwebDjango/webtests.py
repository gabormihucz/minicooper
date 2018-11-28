import unittest
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
        'MCwebDjango.settings')

import django
django.setup()
from django.utils import timezone
from mcwebapp.models import PdfFile


class ModelTest(unittest.TestCase):
    def pdfFileTest(self):
        filename = 'gibberish'
        curr_time = timezone.now()
        pdf = PdfFile(file_name = filename, upload_date = curr_time)
        pdf.save()
        self.assertEqual(PdfFile.objects.get(file_name = filename), pdf)

if __name__ == "__main__":
    unittest.main()
