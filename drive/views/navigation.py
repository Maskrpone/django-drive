from django.shortcuts import render
import os

MAX_FILE_SIZE = 40 * 1024 * 1024 # 40 Mo en octets

def home(request, username, path=""):

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

