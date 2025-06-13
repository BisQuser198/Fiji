# docxcloner/forms.py
from django import forms
# accept input from your visitors -- https://docs.djangoproject.com/en/5.2/topics/forms/
# In HTML, a form is a collection of elements inside <form>...</form> that allow a visitor to do things like enter text, select options, manipulate objects or control
#  form must specify: 
# where: the URL to which the data corresponding to the user’s input should be returned
# how: the HTTP method the data should be returned by
# GET and POST are the only HTTP methods to use when dealing with forms.
# POST  browser bundles up the form data, encodes it for transmission, sends it to the server, and then receives back its response
# GET -- bundles the submitted data into a string, and uses this to compose a URL
#  a request that makes changes in the database - should use POST
#  GET is suitable for things like a web search form
# Django Form class describes a form and determines how it works and appears.
# In a similar way that a model class’s fields map to database fields, a form class’s fields map to HTML form <input> elements.
# form’s fields are themselves classes; they manage form data and perform validation when a form is submitted. A DateField and a FileField handle very different kinds of data
# Instantiating, processing, and rendering forms¶
# When rendering an object in Django, we generally:
# get hold of it in the view (fetch it from the database, for example)
# pass it to the template context
# expand it to HTML markup using template variables

# Key Example: 
# from django import forms
# class NameForm(forms.Form):
#     your_name = forms.CharField(label="Your name", max_length=100)

class CloneDocxForm(forms.Form):
    source_file = forms.FileField(label="Upload Source DOCX") # creates a Form where the user can input Files + labels it (for HTML)
    target_start = forms.IntegerField(label="Starting Target Number", initial=2)
    target_end = forms.IntegerField(label="Ending Target Number", initial=26)

#All you need to do to get your form into a template is to place the form instance into the template context. {{ form }}

# The Template
"""
<form action="/your-name/" method="post">
    {% csrf_token %}
    {{ form }}
    <input type="submit" value="Submit">
</form>
"""

# The view -- views.py
# Form data sent back to a Django website is processed by a view, generally the same view which published the form. 

"""
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import NameForm

def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect("/thanks/")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, "name.html", {"form": form}) 
    """