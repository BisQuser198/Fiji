# Step-by-Step Setup Guide

Follow these steps to add a minimal file-upload app in Django. Uploaded files will be saved and can be processed later on demand.

## 1. Create a Django Project & App

```bash
django-admin startproject fileupload_project
cd fileupload_project
python manage.py startapp uploader
```

## 2. Update `settings.py`

In `fileupload_project/settings.py`:

```python
INSTALLED_APPS = [
    # …
    'uploader',
]

import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Where uploaded files go
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

## 3. Define the Model

Create `uploader/models.py`:

```python
from django.db import models

class Upload(models.Model):
    # Stores the uploaded file
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
```

## 4. Create a Simple Form

Create `uploader/forms.py`:

```python
from django import forms

class UploadForm(forms.Form):
    file = forms.FileField(label='Select a file')
```

## 5. Write a Processing Utility

Create `uploader/utils.py`:

```python
import os, json
import pandas as pd
from docx import Document

def process_file(path):
    """
    Read file at `path` based on extension.
    Returns a one-line summary string.
    """
    ext = os.path.splitext(path)[1].lower()

    if ext == '.csv':
        df = pd.read_csv(path)
        return f'CSV rows: {len(df)}'

    if ext in ('.xls', '.xlsx'):
        df = pd.read_excel(path)
        return f'Excel rows: {len(df)}'

    if ext == '.json':
        data = json.load(open(path))
        count = len(data) if isinstance(data, list) else len(data.keys())
        return f'JSON items: {count}'

    if ext == '.docx':
        doc = Document(path)
        return f'DOCX paragraphs: {len(doc.paragraphs)}'

    return 'Unsupported file type'
```

## 6. Implement Views

Create `uploader/views.py`:

```python
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
            return redirect('upload_list')
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
```

## 7. Configure URLs

Create `uploader/urls.py`:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_file, name='upload_file'),
    path('uploads/', views.upload_list, name='upload_list'),
    path('process/<int:pk>/', views.process_upload, name='process_upload'),
]
```

In `fileupload_project/urls.py`, include and serve media:

```python
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('uploader.urls')),
]

# Serve MEDIA files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

## 8. Create Templates

Under `uploader/templates/uploader/`, add:

**upload.html**
```html
<!DOCTYPE html>
<html>
<head><title>Upload File</title></head>
<body>
  <h1>Upload a File</h1>
  <form method="post" enctype="multipart/form-data">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Upload</button>
  </form>
  <a href="{% url 'upload_list' %}">View Uploaded Files</a>
</body>
</html>
```

**upload_list.html**
```html
<!DOCTYPE html>
<html>
<head><title>Uploaded Files</title></head>
<body>
  <h1>Files</h1>
  <ul>
    {% for u in uploads %}
      <li>
        {{ u.file.name }} ({{ u.uploaded_at }}) —
        <a href="{% url 'process_upload' u.pk %}">Process</a>
      </li>
    {% empty %}
      <li>No files uploaded yet.</li>
    {% endfor %}
  </ul>
  <a href="{% url 'upload_file' %}">Upload More</a>
</body>
</html>
```

## 9. Finalize & Run

```bash
python manage.py makemigrations
python manage.py migrate
mkdir media
python manage.py runserver
```

- Navigate to http://127.0.0.1:8000/upload/  
- Upload any CSV, XLSX, JSON or DOCX  
- Visit “View Uploaded Files” and click “Process” to see your file’s summary  

---

You now have a barebones Django file-upload flow with on-demand server-side processing.