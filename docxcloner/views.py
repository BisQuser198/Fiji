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

"""Attribute Access:
form.cleaned_data uses dot notation to access an attribute called cleaned_data on the form object.
In Django, after a form has been submitted and validated, the form instance has an attribute cleaned_data, which is a dictionary containing all the form fields paired with their cleaned and validated values.
Dictionary Key Access:
Once the code obtains the dictionary (cleaned_data), it uses square bracket notation (['source_file']) to retrieve the value associated with the key 'source_file'.
In this context, 'source_file' is expected to be a field in the form (most likely a file field), and its value will be the uploaded file (typically an instance of UploadedFile in Django).
So, the syntax form.cleaned_data['source_file'] is a combination of accessing an attribute (cleaned_data) from the form object and then using dictionary indexing to extract the value corresponding to the key 'source_file'. In Python, the dot (.) operator is used for accessing attributes of an object, while the square brackets ([]) are used to look up keys in a dictionary."""

# First, obtain the dictionary containing all validated form data.
### cleaned_data = form.cleaned_data

# 'cleaned_data' is a dictionary where the keys match the names of the form fields.
# Now, extract the value associated with the 'source_file' key.
#
# This value represents the uploaded file as processed and validated by the Django form.
### source_file = cleaned_data.get('source_file')


def clone_view(request):
    if request.method == "POST":
        form = CloneDocxForm(request.POST, request.FILES)
        if form.is_valid():
            # Save uploaded file to a temporary location
            source_file = form.cleaned_data['source_file']
            target_start = form.cleaned_data['target_start']
            target_end = form.cleaned_data['target_end'] # -- object.attribute['key'] => access attribute cleaned_data of object form, then treating the attribute
            # as a dictionary and getting the value stored under target_start (expected to the the user_provided starting number from the form input)
            # Access validated data: When a Django form is submitted, it creates a dictionary called cleaned_data containing all the form fields with the values, 
            # form.cleaned_data == {} dictionary. Using the bracket notation ['target_start'] retrieves the value from the {} is expected to be the user-provided 
            # starting target number from the form input
            # expanded & more verbose:
            # if 'target_start' in cleaned_data: target_start = cleaned_data['target_start'] else: target_start = None (or raise error or assign default)

            ## Understanding these two concepts --attribute access via the dot notation and dictionary key access via the square brackets—-is fundamental in Python

            # Create a temporary directory for processing, then extract the file name (source_file.name) and construct the path (source_path == source_file_path)
            temp_dir = tempfile.mkdtemp()  # create a temporary directory 
            # creates a new, uniquely named temporary directory in the system’s temporary files location. It returns the full path (as a string) of the new directory. This directory is useful for storing temporary files during processing. In the given code, temp_dir holds the path to this directory, ensuring that any files we need to write or manipulate only affect this isolated space, reducing the risk of interfering with existing files on the system.
            source_path = os.path.join(temp_dir, source_file.name) # combine the temporary directory with the uploaded file's name
            # os.path.join() function combines one or more path components into a single path.
            # ensures the resulting source_path is a valid file path in the temporary directory - More verbose
            # import os 
            # import tempfile
            # temp_dir = tempfile.mkdtemp()
            # 'temp_dir' now holds the path, e.g., '/tmp/tmpabcd1234'
            # 'source_file' is expected to be an object representing the uploaded file, 
            # and it has an attribute 'name' which contains the original filename.
            # uploaded_file_name = source_file.name
            # 3 construct full file path
            # 'os.path.join' combines the temporary directory and the uploaded file's name into a single path.
            # 'os.path.join' combines the temporary directory and the uploaded file's name into a single path.
            # source_path = os.path.join(temp_dir, uploaded_file_name)
            # 'source_path' now holds a value like '/tmp/tmpabcd1234/yourfile.docx'

            with open(source_path, 'wb') as f:
                for chunk in source_file.chunks():
                    f.write(chunk)

                    ## is used to write the contents of an uploaded file to disk in a memory-efficient way. Here’s a detailed explanation of how it works:


# source_file.chunks(): When a file is uploaded through a Django form, it is represented by an UploadedFile object. Instead of reading the entire file into memory at once (which can be inefficient or even crash the server with very large files), Django provides the chunks() method. This method returns an iterator that yields small pieces (chunks) of the file, typically of a default size (which can be customized). This allows the file to be processed in parts.

# for chunk in source_file.chunks():: This loop iterates over each chunk produced by the chunks() method. Each iteration provides a segment (or block) of the file’s content rather than the whole file at once.

# f.write(chunk): Within each iteration, the current chunk is written to the file represented by f. Since f was opened in binary write mode ('wb'), each chunk is written directly to disk in the exact order it was read. This ensures that the file is reconstructed correctly from its parts.

# Open the destination file in write-binary mode ('wb') so that 
# the file contents are written as raw bytes.
# with open(source_path, 'wb') as destination_file:
    
    # Retrieve the file data from the uploaded file in chunks.
    # This is helpful for memory management, especially for large files,
    # as it does not require reading the entire file into memory.
    # file_chunks = source_file.chunks()
    
    # Iterate over each chunk (a small segment of the file's contents).
    # for chunk in file_chunks:
        # Write the current chunk to the destination file on disk.
        # This appends the chunk to the file until the entire file is written.
        # destination_file.write(chunk)


# Opening the File: We use a with statement to open the file at source_path in binary write mode ('wb'). The with statement ensures that the file is automatically closed after the block of code executes, even if an error occurs.

# Getting Chunks: The source_file.chunks() method is called, and its result is stored in file_chunks. This iterator will yield a series of chunks from the uploaded file.

# Looping & Writing Chunks: A for loop goes through each chunk returned by file_chunks. For every chunk, we call destination_file.write(chunk) to append that segment to the file on disk.

# This method efficiently handles file uploads by avoiding high memory usage, which is crucial when working with large files in web applications.
            
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
