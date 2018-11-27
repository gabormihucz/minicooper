from django.shortcuts import render
from django.http import HttpResponse

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

    return HttpResponse("Hello world.")
