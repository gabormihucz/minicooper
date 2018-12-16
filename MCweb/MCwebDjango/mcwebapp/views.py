from django.shortcuts import render
from django.http import HttpResponse
from .forms import UserForm
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
import json
from django.shortcuts import get_object_or_404
from django.conf import settings as psettings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from mcwebapp.models import *

# user auth

from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse

from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

import datetime

# helper function that paginates a list
from django.views.decorators.csrf import csrf_exempt
import json
import base64

# importing OCR processing
from mcwebapp.pdf2json import pdf_process

def paginate(input_list, request):
    page = request.GET.get('page', 1)
    paginator = Paginator(input_list, 10)

    try:
        elems = paginator.page(page)
    except PageNotAnInteger:
        elems = paginator.page(1)
    except EmptyPage:
        elems = paginator.page(paginator.num_pages)

    return {'elems': elems}

def index(request):
    # to work with templates:
    # - make a context_dict (standard python dictionary) to pass the data into the template
    # - return render(request, 'mcwebapp/[html file].html', context=context_dict)
    # note that the directory string above points to MCweb/MCwebDjango/templates as root.
    #
    # to access the values from inside the HTML:
    # - {{ [dictionary key] }}
    #
    # to use static files (like the logo image):
    # - write {% load staticfiles %} right before <html>
    # - for a picture static/images/cat/jpg
    #       <img src="{% static "images/cat.jpg" %}" alt="picture of a cat">
    # @2277073z

    # as user who is not logged in is redirected to the login page
    # superuser in case of no templates is redirected to the template creator page
    # otherwise return a view with the list of jsons paginated

    if request.user.is_anonymous:
        return HttpResponseRedirect("/accounts/login")
    if not TemplateFile.objects.all() and request.user.is_superuser:
        return HttpResponseRedirect("/dummy_creator/")

    jsons = JSONFile.objects.all()
    context_dict = paginate(jsons, request)

    response = render(request,'mcwebapp/index.html',context_dict)
    return response

def dummy_creator(request):
    return render(request,'mcwebapp/dummy_creator.html',{})


#view required to handle POST request from mcApp. We still need to tackle how we will recognize how post is linked to a user, so far authentication not required
@csrf_exempt
def upload_pdf(request):
    if request.method =="POST":
        #decoding post message
        json_post = request.body.decode('utf-8')
        #translating json into python dictionary
        data = json.loads(json_post)

        #retranslating binary of the pdf into a system readable bytes
        content = data["content"].encode('utf-8')
        content = base64.b64decode(content)


        name = data["filename"]
        upload_date = datetime.datetime.now()
        #TODO so far it works with precreated template, edit later
        template = TemplateFile.objects.get(name="SampleTemplate")

        #creating a pdf in media/pdffiles
        with open("media/pdfFiles/"+name+".pdf", "wb") as o:
            o.write(content)

        #creating model instance
        pdfFile = PDFFile()
        pdfFile.name=name
        pdfFile.upload_date=upload_date
        pdfFile.file_name.name = "pdfFiles/"+name+".pdf" #black magic use this for help: https://stackoverflow.com/questions/7514964/django-how-to-create-a-file-and-save-it-to-a-models-filefield
        pdfFile.template=template

        pdfFile.save()

        pdf_process.pdf_proccess(template.name,"media/templateFiles/", name,"media/pdfFiles/", "media/jsonFiles/")

        # creating json model instance
        jsonFile = JSONFile()
        jsonFile.name = name
        jsonFile.upload_date = upload_date
        jsonFile.file_name.name = "jsonFiles/" + name + ".json"
        jsonFile.pdf = pdfFile

        return HttpResponse("Post request parsed succesfully")
    #if not a post visualise the template that is responsible for handeling posts
    return render(request,'mcwebapp/uploadPDF.html',{})


@csrf_exempt
def get_pdf_info(request):
    if request.method =="GET":
        #assigning the value of a parameter to a variable
        file_name = request.GET.get('file_name','url query with no or wrong parameters') #the second part is whatto return when parameter is wrongly structure

        try:
            #trying to find a right object
            response = PDFFile.objects.get(name=file_name)
            return HttpResponse("File exist")
            # jsonresp = json.dumps(response)

        except:
            return HttpResponse("File not stored on the server")

    #regular subpage to visit if get not send
    return render(request,'mcwebapp/getPDFInfo.html',{})
