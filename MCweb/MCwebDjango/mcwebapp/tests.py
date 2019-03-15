from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

import unittest
import urllib.request, json, datetime, pytz, populate

from mcwebapp.models import *
from mcwebapp.pdf2json import pdf_process, crop


import urllib.request
import json
import base64
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


class GetMoreTablesTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.user.save()
        self.client.force_login(self.user)

    def test_get_more_tables_redirect(self):
        response = self.client.get(reverse('get_more_tables'))
        # get more tables should respond OK after having logged in
        self.assertEqual(response.status_code, 200)


class SaveTemplateTest(TestCase):

    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        User.objects.create_user(**self.credentials)


    def testPost(self):
        c = Client()
        c.login(username='testuser', password='secret')
        body = {"template_name":"testTemp","rectangles":{"default0":{"x1":213,"y1":78,"x2":398,"y2":225,"mandatory":"true"}}}
        response = c.post('/template_creator/',body, content_type="application/json")
        self.assertEqual(response.content.decode('utf-8')[0:2],"OK")


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
        c = Client()
        c.login(username='testuser', password='secret')
        template = TemplateFile.objects.get(name="SampleTemplate")
        response = c.get('/template_editor/'+str(template.id), follow=True)
        self.assertEqual(response.context.get("JSON")["name"], "SampleTemplate")

    def test_template_editor_with_non_existent_template(self):
        # test checks if asking for a non-existent template returns correct HttpResponse
        c = Client()
        c.login(username='testuser', password='secret')
        response = c.get('/template_editor/999999999999999999999999999999999999', follow=True)
        self.assertEqual(response.content.decode('utf-8'),"Template could not be found")

    def test_template_editor_owerwriting_a_template_with_a_name_of_a_template_which_already_exist(self):
        # test checks if asking for a non-existent template returns correct HttpResponse
        templateOriginal = TemplateFile.objects.create(name="OriginalTestTemplate",upload_date=timezone.now(),
                                    user=User.objects.get(username = 'testuser'))

        templateInEdition = TemplateFile.objects.create(name="templateInEdition",upload_date=timezone.now(),
                                    user=User.objects.get(username='testuser'))

        c = Client()
        c.login(username='testuser', password='secret')
        body = {"template_name":"OriginalTestTemplate","template_id":str(templateInEdition.id),"rectangles":{"default0":{"x1":213,"y1":78,"x2":398,"y2":225,"mandatory":"true"}}}
        response = c.post('/template_editor/'+str(templateInEdition.id) ,body, content_type="application/json")
        self.assertEqual(response.content.decode('utf-8'),"A template with this name already exists, please pick a new name")

    def test_template_editor_owerwriting_a_template_with_a_new_template_name(self):
        # test checks if asking for a non-existent template returns correct HttpResponse
        testedTemplate = TemplateFile.objects.create(name="testedTemplate",upload_date=timezone.now(),
                                    user=User.objects.get(username='testuser'))

        c = Client()
        c.login(username='testuser', password='secret')
        body = {"template_name":"testedTemplatedWithNewName","template_id":str(testedTemplate.id),"rectangles":{"default0":{"x1":213,"y1":78,"x2":398,"y2":225,"mandatory":"true"}}}
        response = c.post('/template_editor/'+str(testedTemplate.id) ,body, content_type="application/json")
        self.assertEqual(response.content.decode('utf-8')[:2],"OK")
        os.remove("media/templateFiles/testedTemplatedWithNewName.json")

    def test_template_editor_owerwriting_a_template_without_changing_a_name(self):
        # test checks if asking for a non-existent template returns correct HttpResponse
        testedTemplate = TemplateFile.objects.create(name="testedTemplateWithSetName",upload_date=timezone.now(),
                                    user=User.objects.get(username='testuser'))

        c = Client()
        c.login(username='testuser', password='secret')
        body = {"template_name":"testedTemplateWithSetName","template_id":str(testedTemplate.id),"rectangles":{"default0":{"x1":214,"y1":78,"x2":398,"y2":225,"mandatory":"true"}}}
        response = c.post('/template_editor/'+str(testedTemplate.id) ,body, content_type="application/json")
        self.assertEqual(response.content.decode('utf-8')[:2],"OK")
        os.remove("media/templateFiles/testedTemplateWithSetName.json")

#following test determines if the core functionallity of a website, that is processing uploaded pdf's and extracting data with regard to a predefined temlate works
class UploadPdfTest(TestCase):

    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        User.objects.create_user(**self.credentials)
        template = TemplateFile.objects.create(name="SampleTemplate",upload_date=timezone.now(),
                                    user=User.objects.get(username = 'testuser'))
        MatchPattern.objects.create(regex="test", template=template)

    # testing if code fails if not relevant pdf is uploaded
    def testPostWrongPdf(self):
        c = Client()
        data = "SGVsbG8gSSBhbSBhIHBkZiBtYWRlIGZvciB0ZXN0IHB1cnBvc2UK"
        body = {"filename":"testPdf","content":data}
        c.login(username='testuser', password='secret')
        response = c.post('/upload_pdf/',body,content_type="application/json")

        self.assertEqual(response.content.decode('utf-8'),"Pdf sent over post seems to be corrupted")

    # check if the Pdf has been assigned the correct template
    def testPdfToTemplateMatching(self):
        # Creating a template file that will be used to create a DB instance of template model
        with open("media/templateFiles/template_testfile.json", "w") as t:
            dictJson = {'default0': {'x1': 76, 'y1': 73, 'x2': 143, 'y2': 88, 'mandatory': True}, 'size': {'x': 596, 'y': 843}}
            t.write(json.dumps(dictJson,ensure_ascii=False))

        # creating a DB instance of a template model
        template = TemplateFile.objects.create(name="template_testfile",upload_date=timezone.now(),
                                    user=User.objects.get(username = 'testuser'))
        template.file_name.name = "templateFiles/template_testfile.json"

        # creating a pattern which will link a template with an incoming pdf file
        pattern = MatchPattern.objects.create(regex="upload",template=template)

        # loading binaries of a pdf that will later be uploaded
        with open("mcwebapp/pdfs/testfile.pdf","rb") as f:
            pdf_as_binary = base64.b64encode(f.read())

        # creating a post message that will be send to a server (related view - upload_pdf )
        body = {"filename":"uploadCheck","content":pdf_as_binary.decode('utf-8')}
        c = Client()
        # sending a post
        response = c.post('/upload_pdf/',body,content_type="application/json")

        # opening an output of ocr
        with open("media/jsonFiles/uploadCheck.json","r") as j:
            content = j.read()

        # parsing it from json to get just the related value
        content = json.loads(content)
        content = content["default0"]

        # asserton if post was parsed succesfully and if the output is right
        self.assertEqual(response.content.decode('utf-8'), "Post request parsed succesfully")
        self.assertEqual(content, "Lorem ipsum")

        # rmoving the files that had been created during the test execution
        os.remove("media/jsonFiles/uploadCheck.json")
        os.remove("media/pdfFiles/uploadCheck.pdf")
        os.remove("media/templateFiles/template_testfile.json")

    # testing if html-helper page loads
    def testVisit(self):
        c = Client()
        c.login(username='testuser', password='secret')
        response = self.client.get('/upload_pdf/')
        self.assertEqual(response.status_code, 200)

# this test requires populating the database
# checks if there is any JSONFile, which has the pattern 'File' in it
class SearchTemplateTest(TestCase):

    def setUp(self):
        populate.populate()
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.user.save()
        self.client.force_login(self.user)

    # test passes if the search page returns the status code 200
    def test_search_page_exists(self):
        templates = TemplateFile.objects.filter(name__icontains='Sample')[:10]
        url = reverse('searchTemplates') + "?search-bar=Sample"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    # test passes if search returns correct results
    def test_search_gives_correct_results(self):
        templates = TemplateFile.objects.filter(name__icontains='Sample')[:10]
        url = reverse('searchTemplates') + "?search-bar=Sample"
        response = self.client.get(url)
        self.assertQuerysetEqual(response.context['elems'], [repr(template) for template in templates])


#  check if processing works with single "normal" template
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

#  check if multiple pdfs can be processed without overwriting
class DuplicatePdfProcessTest(TestCase):
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

#  check if, during process, whether or not the mandatory fields are filled is checked
class PdfProcessErrorCheckingTest(TestCase):
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
    def test_mandatory_field_succeeds(self):
        try:
            os.remove("media/jsonFiles/" + "TestPDF" + ".json")
        except OSError:
            pass

        process_dict = pdf_process.pdf_proccess("mandatory_field_succeed_test", "media/templateFiles/", "TestPDF", "media/pdfFiles/", "media/jsonFiles/")
        success = process_dict["mand_filled"]
        os.remove("media/jsonFiles/" + "TestPDF" + ".json")
        self.assertTrue(success)

#  check if processing still works when coordinates are saved in oposite order in the template file
class PdfProcessCoordinateSwitchedTest(TestCase):
    # test passes if processing works correctly with a template where the coordinates of the corners of the template are switched
    def test_corner_switched_template(self):
        try:
            os.remove("media/jsonFiles/" + "TestPDF" + ".json")
        except OSError:
            pass

        process_dict = pdf_process.pdf_proccess("CornerSwitchedTemplate", "media/templateFiles/", "TestPDF", "media/pdfFiles/", "media/jsonFiles/")
        with open("media/jsonFiles/" + "TestPDF" + ".json", "r") as output:
            json_output = json.loads(output.read())

        os.remove("media/jsonFiles/" + "TestPDF" + ".json")

        test_string = {"default1": "Post Code"}
        self.assertEqual(json_output, test_string)

#  check if processing works when fields overlap in the template
class PdfProcessOverlappingFieldsTest(TestCase):
    # test passes if template with overlapping fields processes pdf correctly
    def test_overlapping_fields(self):
        try:
            os.remove("media/jsonFiles/" + "TestPDF" + ".json")
        except OSError:
            pass

        process_dict = pdf_process.pdf_proccess("overlapping_field_test", "media/templateFiles/", "TestPDF", "media/pdfFiles/", "media/jsonFiles/")
        with open("media/jsonFiles/" + "TestPDF" + ".json", "r") as output:
            json_output = json.loads(output.read())

        os.remove("media/jsonFiles/" + "TestPDF" + ".json")

        test_string = {"default0": "Post Code", "default1": "Post Code"}
        self.assertEqual(json_output, test_string)

#  check if processing works when the aspect ratio is differen between the pdf and template
class PdfProcessAspectRatioTest(TestCase):
        # test passes if pdf processes correctly with template of a different aspect ratio
        def test_aspect_ratio(self):
            try:
                os.remove("media/jsonFiles/" + "TestPDF" + ".json")
            except OSError:
                pass

            process_dict = pdf_process.pdf_proccess("aspect_ratio_test", "media/templateFiles/", "TestPDF", "media/pdfFiles/", "media/jsonFiles/")
            with open("media/jsonFiles/" + "TestPDF" + ".json", "r") as output:
                json_output = json.loads(output.read())

            os.remove("media/jsonFiles/" + "TestPDF" + ".json")

            test_string = {"default1": "Sample PDF"}
            self.assertEqual(json_output, test_string)

# tests responsible for checking if actions started in template_manager are correctly executed by a
class ManageTemplatesTest(TestCase):

    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        User.objects.create_user(**self.credentials)
        TemplateFile.objects.create(name="TestTemp",upload_date=timezone.now(),file_name="sth",
                                    user=User.objects.get(username = 'testuser'))


    def test_template_manager_with_pattern_add(self):
        template = TemplateFile.objects.get(name="TestTemp")
        c = Client()
        message = {"code":"addPattern","regex":"TestAddRegex","template_id":template.id}
        c.login(username='testuser', password='secret')
        response = c.post('/template_manager/',message, content_type="application/json")
        self.assertEqual(response.context.get('patterns')[0].regex,"TestAddRegex")

#   test at first add an pattern, then counts how many pattern are there, then deletes the originally created pattern and checks in in an aftermath there is less patterns then before
    def test_template_manager_with_pattern_delete(self):
        template = TemplateFile.objects.get(name="TestTemp")
        c = Client()
        c.login(username='testuser', password='secret')
        message = {"code":"addPattern","regex":"TestDeleteRegex","template_id":template.id}
        response = c.post('/template_manager/',message, content_type="application/json")

        count1 = 0
        testDelPatternId = None
        for pattern in response.context.get('patterns'):
            if pattern.regex=="TestDeleteRegex":
                testDelPatternId = pattern.id
            count1 += 1

        message = {"code":"deletePattern","pattern_id":testDelPatternId}
        response = c.post('/template_manager/',message, content_type="application/json")
        count2 = 0
        for pattern in response.context.get('patterns'):
            count2 += 1

        self.assertFalse(count1==count2)


    def test_template_manager_with_template_delete_request_with_no_releted_files(self):
        template = TemplateFile.objects.create(name="TestTempWithNoRelations",upload_date=timezone.now(),file_name="sth",
                                    user=User.objects.get(username = 'testuser'))
        message = {"code":"deleteTemplate_request","template_id":template.id}
        c = Client()
        c.login(username='testuser', password='secret')
        response = c.post('/template_manager/',message, content_type="application/json")
        self.assertEqual(response.content.decode('utf-8'),"PDF's that will be deleted as a result of deleting a template:\nNo Pdf will be affected\n")

# test checks if backend would warn user about what pdfs ould be deleted along the deleted template
    def test_template_manager_with_template_delete_request_with_releted_files(self):
        template = TemplateFile.objects.create(name="TestTempWithRelations",upload_date=timezone.now(),file_name="sth",
                                    user=User.objects.get(username = 'testuser'))
        pdf = PDFFile.objects.create(name="relatedPDF",upload_date=timezone.now(),file_name=None,template=template)
        message = {"code":"deleteTemplate_request","template_id":template.id}
        c = Client()
        c.login(username='testuser', password='secret')
        response = c.post('/template_manager/',message, content_type="application/json")
        self.assertEqual(response.content.decode('utf-8'),"PDF's that will be deleted as a result of deleting a template:\nrelatedPDF\n")


    def test_template_manager_template_delete(self):
        template = TemplateFile.objects.create(name="TestTempDeleteWithRelations",upload_date=timezone.now(),file_name="sth",
                                    user=User.objects.get(username = 'testuser'))
        pdf = PDFFile.objects.create(name="relatedDeletePDF",upload_date=timezone.now(),file_name=None,template=template)
        message = {"code":"deleteTemplate","template_id":template.id}
        c = Client()
        c.login(username='testuser', password='secret')
        response = c.post('/template_manager/',message, content_type="application/json")
        template_exist = True
        # if templete was properly deleted then error will be raised and template_exist would habe it value changed
        try:
            templateExist = TemplateFile.objects.get(id=template.id)
        except:
            template_exist = False
        self.assertEqual(template_exist,False)

# search templates tests are Aa copy of ManageTemplatesTests
class SearchTemplatesTest(TestCase):

    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        User.objects.create_user(**self.credentials)


    def test_search_template_with_pattern_delete_request_with_no_releted_files(self):
        template = TemplateFile.objects.create(name="TestSearchTempWithNoRelations",upload_date=timezone.now(),file_name="sth",
                                    user=User.objects.get(username = 'testuser'))
        message = {"code":"deleteTemplate_request","template_id":template.id}
        c = Client()
        c.login(username='testuser', password='secret')
        response = c.post('/search_templates/',message, content_type="application/json")
        self.assertEqual(response.content.decode('utf-8'),"PDF's that will be deleted as a result of deleting a template:\nNo Pdf will be affected\n")


    def test_template_manager_with_pattern_delete_request_with_releted_files(self):
        template = TemplateFile.objects.create(name="TestSearchTempWithRelations",upload_date=timezone.now(),file_name="sth",
                                    user=User.objects.get(username = 'testuser'))
        pdf = PDFFile.objects.create(name="relatedSearchPDF",upload_date=timezone.now(),file_name=None,template=template)
        message = {"code":"deleteTemplate_request","template_id":template.id}
        c = Client()
        c.login(username='testuser', password='secret')
        response = c.post('/search_templates/',message, content_type="application/json")
        self.assertEqual(response.content.decode('utf-8'),"PDF's that will be deleted as a result of deleting a template:\nrelatedSearchPDF\n")
