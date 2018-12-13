from django.shortcuts import render
from django.http import HttpResponse
from .forms import UserForm
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
import json
from django.shortcuts import get_object_or_404
from django.conf import settings as psettings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# user auth


from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse

from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from datetime import datetime

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
    if request.user.is_anonymous:
        return HttpResponseRedirect("/accounts/login")

    response = render(request,'mcwebapp/index.html',{})
    return response

def dummy_creator(request):
    return render(request,'mcwebapp/dummy_creator.html',{})
