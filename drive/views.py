from django.shortcuts import render
import os

def home(request, path="", username="maskrpone"):

    base_path = os.path.join("storage", username)

    # Construire le chemin complet en combinant le chemin de base avec le sous-dossier
    full_path = os.path.join(base_path, path)
    files_and_dirs = os.listdir(full_path)
    
    items = []
    for item in files_and_dirs:
        item_full_path = os.path.join(full_path, item)
        if os.path.isdir(item_full_path):
            items.append({"name": item, "is_dir": True})  # C'est un dossier
        else:
            items.append({"name": item, "is_dir": False})  # C'est un fichier

    context = {
        "items": items,
        "current_path": path,
        "username": username,
        "is_root": path == "",
    }
    return render(request, "drive/home.html", context)