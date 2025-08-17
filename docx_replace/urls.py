# docx_replace/urls.py
from django.urls import path
from .views import replace_view

app_name = "docx_replace"

urlpatterns = [
    #path("", replace_view, name="replace_docs"),
    path("", replace_view, name="replace_docs"),
]

## No app_name = … anywhere, and you’re including them without a namespace= argument. 
## That means Django will expose each pattern’s name in the global reverse namespace.