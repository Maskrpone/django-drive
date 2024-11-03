# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings
from django.http import HttpRequest, HttpResponse
from drive.models import Folder
from .forms import SignUpForm
import os

def signup_view(request: HttpRequest) -> HttpResponse:
    """This is the view used to create an account."""
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        
        # We check that the form is valid
        if form.is_valid():
            form.save()
            # Retrieve informations
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            
            # Create a user, stores it and handle sessions
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            create_root_folder(username, user)
            return redirect('drive')  # Redirigez vers une page d'accueil après connexion
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                create_root_folder(username, user)
                return redirect('drive')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def create_root_folder(username: str, user: User) -> None:
    user_dir = os.path.join(settings.MEDIA_ROOT, username)
    if os.path.exists(user_dir):
        print(f"User {username} directory already exists !")
        return
    
    print(f"Creating directory for : {username}")
    os.makedirs(user_dir)
    Folder.objects.create(name=username, owner=user)
    return