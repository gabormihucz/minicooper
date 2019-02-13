from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

import unittest
import urllib.request, json, datetime, pytz, populate

from mcwebapp.models import *
from mcwebapp.pdf2json import pdf_process, crop

import os

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
        # print(response.status_code)
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
    # test passes if the result of pdfprocess on the Sample PDF using the SampleTemplate matches the expected output
    def test_processing_output_correct(self):
        try:
            os.remove("media/jsonFiles/" + "TestPDF" + ".json")
        except OSError:
            pass

        pdf_process.pdf_proccess("SampleTemplate", "media/templateFiles/", "TestPDF", "media/pdfFiles/", "media/jsonFiles/")
        with open("media/jsonFiles/" + "TestPDF" + ".json", "r") as output:
            json_output = json.loads(output.read())

        os.remove("media/jsonFiles/" + "TestPDF" + ".json")

        test_string = {"cost": "£1000", "tax": "£125", "total": "£1125", "address_line1": "Address line 1", "address_line2": "Address line 2", "city": "City", "post_code": "Post Code"}
        self.assertEqual(json_output, test_string)

    # test passes if the json output of a pdf is not overwritten when the pdf is processed again with the same template
    def test_proccess_handles_duplicate_pdf(self):
        try:
            os.remove("media/jsonFiles/" + "TestPDF" + ".json")
        except OSError:
            pass

        try:
            os.remove("media/jsonFiles/" + "TestPDF(2)" + ".json")
        except OSError:
            pass
        pdf_process.pdf_proccess("SampleTemplate", "media/templateFiles/", "TestPDF", "media/pdfFiles/", "media/jsonFiles/")

        pdf_process.pdf_proccess("mandatory_field_fail_test", "media/templateFiles/", "TestPDF", "media/pdfFiles/", "media/jsonFiles/")
        with open("media/jsonFiles/" + "TestPDF" + ".json", "r") as output:
            json_output = json.loads(output.read())

        os.remove("media/jsonFiles/" + "TestPDF" + ".json")
        os.remove("media/jsonFiles/" + "TestPDF(2)" + ".json")

        test_string = {"default0": "£1000", "default1": ""}
        self.assertNotEqual(json_output, test_string)

    # test passes if pdf_process if pdf_process returns false, indicating that a mandatory field was not filled
    def test_mandatory_field_fails(self):
        try:
            os.remove("media/jsonFiles/" + "TestPDF" + ".json")
        except OSError:
            pass
        process_dict = pdf_process.pdf_proccess("mandatory_field_fail_test", "media/templateFiles/", "TestPDF", "media/pdfFiles/", "media/jsonFiles/")
        success = process_dict["mand_filled"]
        os.remove("media/jsonFiles/" + "TestPDF" + ".json")
        self.assertFalse(success)
    # test passes if pdf_process if pdf_process returns true, indicating that all mandatory fields were filled
    def test_mandatory_field_suceeds(self):
        try:
            os.remove("media/jsonFiles/" + "TestPDF" + ".json")
        except OSError:
            pass
        process_dict = pdf_process.pdf_proccess("mandatory_field_succeed_test", "media/templateFiles/", "TestPDF", "media/pdfFiles/", "media/jsonFiles/")
        success = process_dict["mand_filled"]
        os.remove("media/jsonFiles/" + "TestPDF" + ".json")
        self.assertTrue(success)


#Test which checks template_editor() view
class TemplateEditorTest(TestCase):

    def setUp(self):
        populate.populate()
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        User.objects.create_user(**self.credentials)

    def test_template_editor_with_existing_template(self):
        # the populate.py script was ran so SampleTemplate should exist, together with actual .json file with each content
        # test is checking if context_dictionary sent later to view was loaded correctly
        response = self.client.get('/template_editor/SampleTemplate', self.credentials, follow=True)
        self.assertEqual(response.context.get("JSON")["name"], "SampleTemplate")

    def test_template_editor_with_non_existent_template(self):
        # test checks if asking for a non-existent template returns correct HttpResponse
        response = self.client.get('/template_editor/TemplateWhichDefinetelyNotExist', self.credentials, follow=True)
        self.assertEqual(response.content.decode('utf-8'),"Template could not be found")


class ManageTemplatesTest(TestCase):

    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        User.objects.create_user(**self.credentials)
        TemplateFile.objects.create(name="TestTemp",upload_date=timezone.now(),file_name="sth",
                                    user=User.objects.get(username = 'testuser'))
        MatchPattern.objects.create(name="TestMatchPattern",regex="TestRegex",
                                    template=TemplateFile.objects.get(name = 'TestTemp'))


    def test_template_manager_with_pattern_edit(self):
        c = Client()
        message = {"code":"editPattern","pattern_name":"TestMatchPattern","template_name":"TestTemp","edited_name":"TestTempEdited","edited_regex":"TestRegexEdited"}
        c.login(username='testuser', password='secret')
        response = c.post('/template_manager/',message, content_type="application/json")
        self.assertEqual(response.context.get('patterns')[0].name,"TestTempEdited")


    def test_template_manager_with_pattern_edit(self):
        c = Client()
        message = {"code":"editPattern","pattern_name":"TestMatchPattern","template_name":"TestTemp","edited_name":"TestPatternEdited","edited_regex":"TestRegexEdited"}
        c.login(username='testuser', password='secret')
        response = c.post('/template_manager/',message, content_type="application/json")
        self.assertEqual(response.context.get('patterns')[0].name,"TestPatternEdited")


    def test_template_manager_with_pattern_add(self):
        c = Client()
        message = {"code":"addPattern","new_name":"TestAddPattern","new_regex":"TestAddRegex","template_name":"TestTemp"}
        c.login(username='testuser', password='secret')
        response = c.post('/template_manager/',message, content_type="application/json")
        self.assertEqual(response.context.get('patterns')[1].name,"TestAddPattern")


    def test_template_manager_with_pattern_delete(self):
        c = Client()
        message = {"code":"addPattern","new_name":"TestDeletePattern","new_regex":"TestDeleteRegex","template_name":"TestTemp"}
        c.login(username='testuser', password='secret')
        response = c.post('/template_manager/',message, content_type="application/json")

        count1 = 0
        for pattern in response.context.get('patterns'):
            count1 += 1

        message = {"code":"deletePattern","pattern_name":"TestDeletePattern","template_name":"TestTemp"}
        response = c.post('/template_manager/',message, content_type="application/json")

        count2 = 0
        for pattern in response.context.get('patterns'):
            count2 += 1

        self.assertFalse(count1==count2)
