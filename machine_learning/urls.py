# machine_learning/urls.py

from django.urls import path
from machine_learning.views import eth_plot_view, eth_plot_view2

app_name = "machine_learning"

urlpatterns = [
    path("", eth_plot_view, name="eth_plot"),   # open http://127.0.0.1:8000//machine_learning/
    path("eth_plot2", eth_plot_view2, name="eth_plot2"),   # open http://127.0.0.1:8000//machine_learning/eth_plot_view2

]
