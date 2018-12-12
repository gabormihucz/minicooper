from django.test import TestCase
import unittest
from mcwebapp.models import *
from django.urls import reverse
from django.utils import timezone

# Create your tests here.

class IndexViewTests(TestCase):
    def test_index_view(self):

        response = self.client.get(reverse(''))
        self.assertEqual(response.status_code, 200)

class TestUserProfiles(unittest.TestCase):
    def setUp(self):
        self.u1 = User.objects.create(username='user1')
        self.up1 = UserProfile.objects.create(user=self.u1)

    def TestUserNameExists(self):
        self.assertEqual(User.objects.get(username = 'user1').username, 'user1')

    def tearDown(self):
        self.up1.delete()
        self.u1.delete()

class LogInTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        User.objects.create_user(**self.credentials)
    def test_login(self):
        # send login data
        response = self.client.post('/accounts/login/', self.credentials, follow=True)
        # should be logged in now
        self.assertTrue(response.context['user'].is_active)

class ModelTest(unittest.TestCase):
    def pdfFileTest(self):
        filename = 'gibberish'
        curr_time = timezone.now()
        pdf = PdfFile(file_name = filename, upload_date = curr_time)
        pdf.save()
        self.assertEqual(PdfFile.objects.get(file_name = filename), pdf)