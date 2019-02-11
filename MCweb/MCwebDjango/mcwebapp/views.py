from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.conf import settings as psettings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from .forms import UserForm
from mcwebapp.models import *
from mcwebapp.pdf2json import pdf_process

import json, base64, datetime, pytz, os


# helper function for paginated lists

def paginate(input_list, request):
    page = request.GET.get('page', 1)
    paginator = Paginator(input_list, 10)
    elems = paginator.page(page)

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
        return HttpResponseRedirect("/template_creator/")

    jsons = JSONFile.objects.all().order_by('-upload_date')
    context_dict = paginate(jsons, request)

    response = render(request,'mcwebapp/index.html',context_dict)
    return response

# if not superuser redirect to homepage, otherwise go to template creator
def template_creator(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect("/")
    return render(request,'mcwebapp/template_creator.html',{})


def template_editor(request, temp_name):
    try:
        temp = TemplateFile.objects.get(name=temp_name)

        with open("media/"+str(temp.file_name),"r") as t:
            file = t.read()
        tempDictJSON = {"name":temp.name,"upload_date":temp.upload_date,"user":temp.user,"file":file}
        tempDict ={"JSON":tempDictJSON}
        return render(request,'mcwebapp/template_editor.html',tempDict)
    except:
        return HttpResponse("Template could not be found")

# get the search query, and filter JSON files whether the query appears in them
# and return the matching JSON objects in a paginated list
def search(request):
    query = request.GET.get('search-bar', '')
    jsons = JSONFile.objects.filter(name__icontains=query)
    context_dict = paginate(jsons, request)
    return render(request, 'mcwebapp/search_files.html', context_dict)

#start
def search_templates(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        template_manager_code_check(data)

    query = request.GET.get('search-bar', '')
    templates = TemplateFile.objects.filter(name__icontains=query)
    patterns = MatchPattern.objects.all()

    context_dict = paginate(templates, request)
    context_dict['patterns'] = patterns

    return render(request, 'mcwebapp/search_templates.html', context_dict)
#end

def manage_templates(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        template_manager_code_check(data)

    templates = TemplateFile.objects.all()
    patterns = MatchPattern.objects.all()

    context_dict = paginate(templates, request)
    context_dict['patterns'] = patterns
    response = render(request,'mcwebapp/template_manager.html',context_dict)
    return response


@csrf_exempt
def save_template(request):
    if request.method =="POST":
        try:
            print("post request to save template")

            # translating post message json into python dictionary
            data = json.loads(request.body.decode('utf-8'))

            # creating template object
            template = TemplateFile()
            template.name = data["template_name"]
            template.upload_date = timezone.now()

            with open("media/templateFiles/"+data["template_name"]+".json", "w") as o:
                o.write(json.dumps(data["rectangles"], ensure_ascii=False))

            template.file_name.name = "templateFiles/"+data["template_name"]+".json"
            template.user = request.user

            template.save()
            return HttpResponse("Post request parsed succesfully")
            #start
        except:
            return HttpResponse("Template coudn't be save")
            #end
    return render(request,'mcwebapp/saveTemplate.html',{})



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
        upload_date = timezone.now()
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
#start
        try:
            success = pdf_process.pdf_proccess(template.name,"media/templateFiles/", name,"media/pdfFiles/", "media/jsonFiles/")
            # creating json model instance
            jsonFile = JSONFile()
            jsonFile.name = name
            jsonFile.upload_date = upload_date
            jsonFile.file_name.name = "jsonFiles/" + name + ".json"
            jsonFile.pdf = pdfFile

            jsonFile.mandatory_fulfilled = success
            if success:
                jsonFile.status_string = "Pass"
            else:
                jsonFile.status_string = "Fail"

            jsonFile.save()
            return HttpResponse("Post request parsed succesfully")
#end
        except:
            return HttpResponse("Pdf sent over post seems to be corrupted")
    #if not a post visualise the template that is responsible for handeling posts
    return render(request,'mcwebapp/uploadPDF.html',{})


@csrf_exempt
def get_pdf_info(request):
    if request.method =="GET":
        #assigning the value of a parameter to a variable
        file_name = request.GET.get('file_name','url query with no or wrong parameters') #the second part is whatto return when parameter is wrongly structure

        if file_name == 'url query with no or wrong parameters':
             #regular subpage to visit if get not send
             return render(request,'mcwebapp/getPDFInfo.html',{})
        else:
            try:
                #trying to find a right object
                response = PDFFile.objects.get(name=file_name)
                return HttpResponse("File exist")
                # jsonresp = json.dumps(response)
            except:
                return HttpResponse("File not stored on the server")

#helper functions

def template_manager_code_check(data):
    if data['code'] == "editPattern":
        template = TemplateFile.objects.get(name=data["template_name"])
        patternsMatching = MatchPattern.objects.filter(template=template)

        for element in patternsMatching:
            if element.name == data["pattern_name"]:
                pattern = element
                break

        pattern.name=data["edited_name"]
        pattern.regex=data["edited_regex"]
        pattern.save()

    elif data['code'] == "deletePattern":
        template = TemplateFile.objects.get(name=data["template_name"])
        patternsMatching = MatchPattern.objects.filter(template=template)


        for element in patternsMatching:
            if element.name == data["pattern_name"]:
                pattern = element
                pattern.delete()
                break


    elif data['code'] == "addPattern":
        template = TemplateFile.objects.get(name=data["template_name"])
        pattern = MatchPattern()
        pattern.name = data["new_name"]
        pattern.regex = data["new_regex"]
        pattern.template = template
        pattern.save()
