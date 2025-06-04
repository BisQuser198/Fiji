from django.shortcuts import render

# Create your views here.
# docxcloner/views.py
import os
import zipfile
import tempfile
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.shortcuts import render
from .forms import CloneDocxForm
from .docx_utils import clone_docx  # our utility function

def clone_view(request):
    if request.method == "POST":
        form = CloneDocxForm(request.POST, request.FILES)
        if form.is_valid():
            # Save uploaded file to a temporary location
            source_file = form.cleaned_data['source_file']
            target_start = form.cleaned_data['target_start']
            target_end = form.cleaned_data['target_end']
            
            # Create a temporary directory for processing
            temp_dir = tempfile.mkdtemp()
            source_path = os.path.join(temp_dir, source_file.name)
            
            with open(source_path, 'wb') as f:
                for chunk in source_file.chunks():
                    f.write(chunk)
            
            # Clone the DOCX file. This returns a list of file paths.
            new_files = clone_docx(source_path, target_start, target_end)
            
            # Create a zip file containing the cloned files
            zip_filename = os.path.join(temp_dir, "cloned_files.zip")
            with zipfile.ZipFile(zip_filename, 'w') as zf:
                for file_path in new_files:
                    # Write each cloned file with its basename into the zip
                    zf.write(file_path, arcname=os.path.basename(file_path))
            
            # Return the zip file as a file response for download
            response = FileResponse(open(zip_filename, 'rb'), as_attachment=True, filename='cloned_files.zip')
            return response
    else:
        form = CloneDocxForm()
    return render(request, "docxcloner/clone.html", {"form": form})
