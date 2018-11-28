from django.shortcuts import render
from django.http import HttpResponse
from .forms import UserForm

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

    return render(request,'mcwebapp/index.html',{})


def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)

        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            registered = True
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()

    context_dict = {'user_form': user_form
                    'registered': registered}
    return render(request, 'mcwebapp/register.html', context_dict)
