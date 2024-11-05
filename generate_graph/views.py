from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.db.models.functions import TruncDate
from django.db.models import Sum
from drive.models import File
from .generate_chart import generate_combined_chart
import base64
from io import BytesIO
import matplotlib.pyplot as plt

def get_number_of_files_by_type(user: User): 
    types = File.objects.filter(owner=user).values_list('file_type', flat=True).distinct()
    
    all_types = {}
    
    for type in types:
        nb_files = File.objects.filter(owner=user, file_type=type).count()
        type = type.split('/')[-1].split('.')[-1]
        if type in ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff']:
            type = 'image'
        
        if type in all_types:
            all_types[type] += nb_files
        else:
            all_types[type] = nb_files
        
    print(f"We have per types : {all_types}")
    return all_types

def generate_types_graph(types: dict):
    labels = list(types.keys())
    values = list(types.values())

    plt.figure(figsize=(7,4))
    plt.bar(labels, values, width=0.4)
    plt.gca().yaxis.get_major_locator().set_params(integer=True)
    plt.xlabel('Formats')
    plt.ylabel('Nombre de documents')
    plt.title("Nombre de documents par types")
    
    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    
    return base64.b64encode(buf.getvalue()).decode('utf-8')

def generate_user_size_graph(user: User):
    files_size = File.objects.filter(owner=user).values_list('size', flat=True)
    total_size = sum(files_size) / 1024 # in Mo
    
    plt.figure(figsize=(7,4))
    plt.pie([100 - total_size, total_size], labels=['Free space', 'Used space'], autopct='%1.1f%%')
    plt.title("Espace total utilisé (max 100 Mo)")
    
    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    
    return base64.b64encode(buf.getvalue()).decode('utf-8')

def generate_timeline_graph(user: User):
     # Truncate the uploaded_at field to the date part and count the number of files for each date
    files_by_date = File.objects.filter(owner=user).annotate(date=TruncDate('uploaded_at')).values('date').annotate(total_size=Sum("size")).order_by('date')
    
    # Prepare data for the graph
    dates = [entry['date'].strftime('%Y-%m-%d') for entry in files_by_date]
    file_counts = [entry['total_size'] for entry in files_by_date]
    
    plt.figure(figsize=(7,4))
    plt.plot(dates, file_counts)
    plt.xlabel("Date")
    plt.ylabel("Total size (Mo)")
    plt.title("Total size of File uploaded over time")
    
    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf-8')
    

def account_info(request):
    types = get_number_of_files_by_type(request.user)
    type_graph = generate_types_graph(types)
    
    size_graph = generate_user_size_graph(request.user)
    
    test = generate_timeline_graph(request.user)
    
    return render(request, 'account_info.html', {'type_chart': type_graph, 'size_chart': size_graph, 'test': test})

