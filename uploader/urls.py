from django.urls import path
from uploader.views import upload_file, upload_list, process_upload

app_name = "uploader"

urlpatterns = [
    path('upload/', upload_file, name='upload_file'),
    path('uploads/', upload_list, name='upload_list'),
    path('process/<int:pk>/', process_upload, name='process_upload'),
]
