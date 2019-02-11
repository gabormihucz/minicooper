from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

import unittest
import urllib.request, json, datetime, pytz, populate

from mcwebapp.models import *
from mcwebapp.pdf2json import pdf_process, crop


# Create your tests here.

class IndexViewTestAnonymous(TestCase):
    def test_index_view_anonymous_redirect(self):
        response = self.client.get(reverse(''))
        # anonymous user should be redirected from homepage
        self.assertEqual(response.status_code, 302)
    def test_index_view_anonymous_redirected_to_login_page(self):
        # after redirecting, the anonymous user should get
        response = self.client.get('', follow=True)
        # the response 200 (the login page)
        self.assertEqual(response.status_code, 200)

class IndexViewTestLoggedIn(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'testuser2',
            'password': 'secret2'}
        User.objects.create_user(**self.credentials)
    def test_login_logged_in(self):
        # send login data
        self.client.post('/accounts/login/', self.credentials, follow=True)
        response = self.client.get(reverse(''))
        # logged in user should get HTTP 200 from the homepage
        self.assertEqual(response.status_code, 200)

class TemplateCreatorViewTestLoggedIn(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'testuser2',
            'password': 'secret2'}
        User.objects.create_user(**self.credentials)
    def test_template_creator_redirects(self):
        # send login data
        self.client.post('/accounts/login/', self.credentials, follow=True)
        response = self.client.get(reverse('template_creator'))
        # normal user should be redirected when attempting to go to the template creator
        self.assertEqual(response.status_code, 302)
    def test_template_creator_redirects_to_homepage(self):
        # send login data
        self.client.post('/accounts/login/', self.credentials, follow=True)
        response = self.client.get(reverse('template_creator'), follow=True)
        # after redirection, normal user should get the status code 200 on the homepage
        self.assertEqual(response.status_code, 200)

# this should be run on an empty database (pdf-json wise), hence before running populate.py
class LogInTestAsSuperUserOnEmptyDatabase(TestCase):
    def setUp(self):

        self.credentials = {
            'username': 'admin12',
            'email'   : 'yolo@yolo.yolo',
            'password': 'pass2'}

        self.adminuser = User.objects.create_superuser(**self.credentials)
        self.adminuser.save()
        self.adminuser.is_staff = True
        self.adminuser.save()
    def test_superuser_is_redirected(self):
        # send login data
        self.client.post('/accounts/login/', self.credentials, follow=True)
        response = self.client.get(reverse(''))
        # since superuser and no files in the results page redirect
        self.assertEqual(response.status_code, 302)
    def test_superuser_is_redirected_to_template_creator_page(self):
        # send login data
        self.client.post('/accounts/login/', self.credentials, follow=True)
        response = self.client.get(reverse(''), follow=True)
        # user should get status code 200 following the redirect
        self.assertEqual(response.status_code, 200)


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

class SaveTemplateTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        User.objects.create_user(**self.credentials)

    def testPost(self):
        c = Client()
        body = {"template_name":"testTemp","rectangles":{"default0":{"x1":213,"y1":78,"x2":398,"y2":225,"mandatory":"true"}}}
        c.login(username='testuser', password='secret')
        response = c.post('/save_template/',body, content_type="application/json")
        self.assertEqual(response.content.decode('utf-8'),"Post request parsed succesfully")

    def testVisit(self):
        response = self.client.get('/save_template/')
        self.assertEqual(response.status_code, 200)

class UploadPdfTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        User.objects.create_user(**self.credentials)
        TemplateFile.objects.create(name="SampleTemplate",upload_date=timezone.now(),
                                    user=User.objects.get(username = 'testuser'))
    def testPost(self):
        c = Client()
        data = "SGVsbG8gSSBhbSBhIHBkZiBtYWRlIGZvciB0ZXN0IHB1cnBvc2UK"
        body = {"filename":"testPdf","content":data}
        c.login(username='testuser', password='secret')
        response = c.post('/upload_pdf/',body,content_type="application/json")

        self.assertEqual(response.content.decode('utf-8'),"Pdf sent over post seems to be corrupted")

    def testVisit(self):
        response = self.client.get('/upload_pdf/')
        self.assertEqual(response.status_code, 200)

class GetPdfInfoTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        User.objects.create_user(**self.credentials)
        TemplateFile.objects.create(name="testTemp",upload_date=timezone.now(),
                                    user=User.objects.get(username = 'testuser'))
        PDFFile.objects.create(name="testPdf",upload_date=timezone.now(),
                                template=TemplateFile.objects.get(name='testTemp'))

    def testGetExistingFile(self):
        c = Client()
        response = c.get("/get_pdf_info/?file_name=testPdf")
        self.assertEqual(response.content.decode('utf-8'),"File exist")

    def testGetNotExistingFile(self):
        c = Client()
        response = c.get("/get_pdf_info/?file_name=notFileLikeThis123456")
        self.assertEqual(response.content.decode('utf-8'),"File not stored on the server")

    def testVisit(self):
        response = self.client.get('/get_pdf_info/')
        print(response.status_code)
        self.assertEqual(response.status_code, 200)

# this test requires populating the database
# checks if there is any JSONFile, which has the pattern 'File' in it
class SearchTest(TestCase):
    def setUp(self):
        populate.populate()
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        User.objects.create_user(**self.credentials)
    # test passes if the search page returns the status code 200
    def test_search_page_exists(self):
        files = JSONFile.objects.filter(name__icontains='File')[:10]
        url = reverse('search_files') + "?search-bar=File"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    # test passes if search returns correct results
    def test_search_gives_correct_results(self):
        files = JSONFile.objects.filter(name__icontains='File')[:10]
        url = reverse('search_files') + "?search-bar=File"
        response = self.client.get(url)
        self.assertQuerysetEqual(response.context['elems'], [repr(elt) for elt in files])


class PdfProcessTest(TestCase):
    def test_processing_output_correct(self):
        pdf_process.pdf_proccess("SampleTemplate", "media/templateFiles/", "SamplePDF", "media/pdfFiles/", "media/jsonFiles/")
        with open("media/jsonFiles/" + "SamplePDF" + ".json", "r") as template:
            json_output = json.loads(template.read())
        test_string = {"cost": "£1000", "tax": "£125", "total": "£1125", "address_line1": "Address line 1", "address_line2": "Address line 2", "city": "City", "post_code": "Post Code"}
        self.assertEqual(json_output, test_string)

#this test does not work hence, commenting it out
    def test_mandatory_field_fails(self):
        success = pdf_process.pdf_proccess("mandatory_field_fail_test", "media/templateFiles/", "SamplePDF", "media/pdfFiles/", "media/jsonFiles/")
        self.assertFalse(success)

    def test_mandatory_field_suceeds(self):
        success = pdf_process.pdf_proccess("mandatory_field_succeed_test", "media/templateFiles/", "SamplePDF", "media/pdfFiles/", "media/jsonFiles/")
        self.assertTrue(success)
