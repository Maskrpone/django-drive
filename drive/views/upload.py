from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest
from django.conf import settings
import os

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