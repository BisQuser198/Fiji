"""
URL configuration for Fiji project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include
from django.shortcuts import render # getting landing page to work


urlpatterns = [
    path('admin/', admin.site.urls),
    # ... your other URLs
    #path('clone_files/', include('clone_files.urls')),
    path('clone_files/', include('clone_files.urls', namespace="clone_files")),
    path('docxcloner/', include('docxcloner.urls')),
    #path('investment/', include("investments.urls")),
    path("investment/", include("investments.urls", namespace="investments")),
    # path("docx_replace/", include("docx_replace.urls")),
    path("replace-docs/", include("docx_replace.urls", namespace="docx_replace")),
    path("dates/", include("dates.urls")),
    path("", lambda request: render(request, "core/landing_page.html"), name="home"),
    path("file_renamer/", include("file_renamer.urls", namespace="file_renamer")),
    path("uploader/", include("uploader.urls", namespace="uploader")),
    path("CS_game/", include("CS_game.urls", namespace="CS_game")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


