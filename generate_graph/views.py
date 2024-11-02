from django.http import JsonResponse
from django.shortcuts import render
from .generate_chart import generate_combined_chart

def account_info(request):
    return render(request, 'account_info.html')  # Assurez-vous que le template est bien dans templates/

def generate_graph_ajax(request):
    folder_path = "storage/hippolyte"
    chart_base64 = generate_combined_chart(folder_path)
    return JsonResponse({'chart': chart_base64})
