from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Upload # Upload class objects store the files
from .forms import UploadForm
from .utils import process_file

def upload_file(request): # accept incoming HTTP request and returns redirect
    # Display empty form / handle POST
    if request.method == 'POST': # enter POST branch only when client submits form / data
        form = UploadForm(request.POST, request.FILES) # instantiate UploadForm (forms.FileField) with POST data 
        if form.is_valid(): # request.FILES contains uploaded files
            Upload.objects.create(file=form.cleaned_data['file'])
            return redirect('uploader:upload_list')
    else:
        form = UploadForm() # instantiate empty form for GET request
    return render(request, 'uploader/upload.html', {'form': form})
# render syntax: render(request, template_name, context) -- context is a dict mapping template variable names to Python objects
# form variable calls UploadForm() - empty object

def upload_list(request):
    # List all uploaded files
    uploads = Upload.objects.all().order_by('-uploaded_at')
    return render(request, 'uploader/upload_list.html', {'uploads': uploads})

def process_upload(request, pk):
    # Process a saved file on demand
    upl = get_object_or_404(Upload, pk=pk)
    result = process_file(upl.file.path)
    return HttpResponse(result)
