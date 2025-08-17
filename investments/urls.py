# investments/urls.py
from django.urls import path
from .views import investment_view

app_name = "investments"        # ← this is your namespace

urlpatterns = [
    #path("", investment_view, name="investment"),
    path("", investment_view, name="form"),  
    # now {% url 'investments:form' %} → /calculator/ (see step 2)
]

