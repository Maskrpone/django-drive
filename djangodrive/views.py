# myproject/views.py

from django.shortcuts import redirect

def home_view(request):
    return redirect("drive_root")