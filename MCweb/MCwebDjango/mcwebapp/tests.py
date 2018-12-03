from django.test import TestCase
import unittest
from mcwebapp.models import *

# Create your tests here.

from django.urls import reverse
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