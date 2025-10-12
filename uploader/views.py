from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Upload
from .forms import UploadForm
from .utils import process_file

def upload_file(request):
    # Display empty form / handle POST
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            Upload.objects.create(file=form.cleaned_data['file'])
            return redirect('uploader:upload_list')
    else:
        form = UploadForm()
    return render(request, 'uploader/upload.html', {'form': form})

def upload_list(request):
    # List all uploaded files
    uploads = Upload.objects.all().order_by('-uploaded_at')
    return render(request, 'uploader/upload_list.html', {'uploads': uploads})

def process_upload(request, pk):
    # Process a saved file on demand
    upl = get_object_or_404(Upload, pk=pk)
    result = process_file(upl.file.path)
    return HttpResponse(result)
