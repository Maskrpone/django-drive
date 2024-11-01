from django.shortcuts import render
from .generate_chart import generate_storage_chart

def account_info(request):
    # Exemple de données pour le graphique
    data = {
        "Images": 500,
        "Documents": 300,
        "Vidéos": 200,
        "Autres": 100,
    }
    chart = generate_storage_chart(data)
    
    return render(request, 'account_info.html', {'chart': chart})
