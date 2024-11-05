from django.http import JsonResponse
from django.shortcuts import render
from .generate_chart import generate_combined_chart

def account_info(request):
    folder_path = "storage/hippolyte"
    chart_base64 = generate_combined_chart(folder_path)
    
    return render(request, 'account_info.html', {'chart': chart_base64})

def generate_graph_ajax(request):
    folder_path = "storage/hippolyte"
    chart_base64 = generate_combined_chart(folder_path)
    return JsonResponse({'chart': chart_base64})
