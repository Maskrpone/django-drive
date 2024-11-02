from django.urls import path
from .views import account_info, generate_graph_ajax

urlpatterns = [
    path('', account_info, name='account_info'),  # URL de la page principale de compte (sans "account/")
    path('generate_graph/', generate_graph_ajax, name='generate_graph'),  # URL pour l'AJAX
]
