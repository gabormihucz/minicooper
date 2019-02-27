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

import json, base64, datetime, pytz, os, re


# helper function for paginated lists

def paginate(input_list, request):
    page = request.GET.get('page', 1)
    paginator = Paginator(input_list, 10)
    elems = paginator.page(page)

    return {'elems': elems}

@login_required
def index(request):
    if not TemplateFile.objects.all() and request.user.is_superuser:
        return HttpResponseRedirect("/template_creator/")

    jsons = JSONFile.objects.all().order_by('-upload_date')
    context_dict = {'elems':jsons}

    response = render(request,'mcwebapp/index.html',context_dict)
    return response

#helper html file for ajax call (in index.html)
@login_required
def get_more_tables(request):
    jsons = JSONFile.objects.all().order_by('-upload_date')
    return render(request, 'mcwebapp/get_more_tables.html', {'elems': jsons})


def json_popup(request, json_slug):
    context_dict = {}
    json = JSONFile.objects.get(slug = json_slug)
    context_dict['json'] = json

    return render(request, 'mcwebapp/json_popup.html', context_dict)

@login_required
# if not superuser redirect to homepage, otherwise go to template creator
def template_creator(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect("/")
    return render(request,'mcwebapp/template_creator.html',{})

@login_required
def template_editor(request, temp_id=-1):
    #if uuser overwrites a template, it reads the request as a post, removes the old json representing old template,
    # create a new one and update the fields of an old template
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        template = TemplateFile.objects.get(id=data['template_id'])
        os.remove("media/templateFiles/"+template.name+".json")
        template.name = data['template_name']
        with open("media/templateFiles/"+data["template_name"]+".json", "w") as o:
            o.write(json.dumps(data["rectangles"], ensure_ascii=False))
        template.file_name.name = "templateFiles/"+data["template_name"]+".json"
        template.save()

        return HttpResponse("http://127.0.0.1:8000/template_manager/")
    #Trying to preload a template so that it's fields can be seen by editor_script.js
    try:
        temp = TemplateFile.objects.get(id=temp_id)
        with open("media/"+str(temp.file_name),"r") as t:
            file = t.read()
        tempDictJSON = {"id":temp.id,"name":temp.name,"upload_date":temp.upload_date,"user":temp.user,"file":file}
        tempDict ={"JSON":tempDictJSON}
        return render(request,'mcwebapp/template_editor.html',tempDict)
    except:
        return HttpResponse("Template could not be found")

@login_required
# get the search query, and filter JSON files whether the query appears in them
# and return the matching JSON objects in a paginated list
def search(request):
    query = request.GET.get('search-bar', '')
    jsons = JSONFile.objects.filter(name__icontains=query)
    context_dict = paginate(jsons, request)
    return render(request, 'mcwebapp/search_files.html', context_dict)

@login_required
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

@login_required
def manage_templates(request, temp_id=-1):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        template_manager_code_check(data)

    templates = TemplateFile.objects.all()
    patterns = MatchPattern.objects.all()

    context_dict = paginate(templates, request)
    context_dict['patterns'] = patterns
    context_dict['unfolded_row'] = int(temp_id)
    response = render(request,'mcwebapp/template_manager.html',context_dict)
    return response


@csrf_exempt
def save_template(request):
    if request.method =="POST":
        try:
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
            return HttpResponse("OKhttp://127.0.0.1:8000/template_manager/"+str(template.id))
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
        # Look through all MatchPatterns
        for pattern in MatchPattern.objects.all():
            match = re.findall(pattern.regex, name)
            if match:  # if a match is found
                template = pattern.template      # get the associated template
                print("I found a template for " + name)
                break                            # leave the loop

        # if no match was found, use the sample template
        if not match:
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
            process_dict = pdf_process.pdf_proccess(template.name,"media/templateFiles/", name,"media/pdfFiles/", "media/jsonFiles/")
            success = process_dict["mand_filled"]
            copies = process_dict["copies"]
            if copies == 1:
                Jname = name
            else:
                Jname = name + "(" + str(copies) + ")"
            # creating json model instance
            jsonFile = JSONFile()
            jsonFile.name = Jname
            jsonFile.upload_date = upload_date
            jsonFile.file_name.name = "jsonFiles/" + Jname + ".json"
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

#helper functions

def template_manager_code_check(data):
    if data['code'] == "deletePattern":
        pattern = MatchPattern.objects.filter(id=data['pattern_id'])
        pattern.delete()

    elif data['code'] == "addPattern":
        template = TemplateFile.objects.get(id=data["template_id"])
        pattern = MatchPattern()
        pattern.regex = data["regex"]
        pattern.template = template
        pattern.save()

    elif data["code"] == "deleteTemplate":
        template = TemplateFile.objects.get(id=data["template_id"])
        template.delete()
