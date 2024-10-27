# myproject/views.py

from django.shortcuts import render

def home_view(request):
    return render(request, 'drive/path.html')