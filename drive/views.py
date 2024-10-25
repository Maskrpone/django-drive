from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest
from django.conf import settings
import os

MAX_FILE_SIZE = 40 * 1024 * 1024 # 40 Mo en octets

def home(request, path="", username="maskrpone"):

    base_path = os.path.join("storage", username)
    full_path = os.path.join(base_path, path)
    
    files_and_dirs = os.listdir(full_path)
    
    items = []
    for item in files_and_dirs:
        item_full_path = os.path.join(full_path, item)
        if os.path.isdir(item_full_path):
            items.append({"name": item, "is_dir": True})
        else:
            items.append({"name": item, "is_dir": False})

    context = {
        "items": items,
        "current_path": path,
        "username": username,
        "is_root": path == "",
    }
    return render(request, "drive/home.html", context)

def folder_contents(request, username, path=""):
    return home(request, path, username)

def upload(request, username, path=""):
    # On n'accepte que les requêtes POST, un fichier est aussi nécessaire
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid request: POST method.")
    if request.FILES.get("filename") is None:
        return HttpResponseBadRequest("Invalid request: file required.")
    
    file = request.FILES["filename"]
    # Le fichier ne doit pas dépasser 40Mo
    if file.size > MAX_FILE_SIZE:
        return HttpResponseBadRequest("File size exceed 40Mo.")
    
    # Définition du chemin jusqu'au fichier
    base_path = os.path.join("storage", username)
    full_path = os.path.join(base_path, path)
    file_path = os.path.join(full_path, file.name)
    
    with open(file_path, "wb+") as destination:
        for chunk in file.chunks():
            destination.write(chunk)
        
    return redirect("folder_contents", username=username, path=path)