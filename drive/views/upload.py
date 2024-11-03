import os
from django.shortcuts import redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseBadRequest
from ..forms import FileUploadForm
from ..models import Folder

MAX_STORAGE_LIMIT = 100 * 1024 * 1024  # 100 MB

def upload_file(request):
    if request.method == "POST":
        form = FileUploadForm(request.POST, request.FILES)
        path = request.POST.get("current_path")
        base_dir = os.path.join(settings.MEDIA_ROOT, request.user.username)
        
        if path:
           folder_path = os.path.join(base_dir, path)
        else:
           folder_path = base_dir
        
        os.makedirs(folder_path, exist_ok=True)

        if form.is_valid():
            uploaded_file = request.FILES["file"]
            if uploaded_file.size > 40 * 1024 * 1024:
                return HttpResponseBadRequest("File size exceeds 40MB limit")
            user_folder_size = get_user_folder_size(folder_path)
            if user_folder_size + uploaded_file.size > MAX_STORAGE_LIMIT:
                return HttpResponseBadRequest("Storage limit of 100MB exceeded")
            fs = FileSystemStorage(location=folder_path)
            fs.save(uploaded_file.name, uploaded_file)
        else:
            return HttpResponseBadRequest("Invalid form")
        if path:
            return redirect("drive", path=path)
    return redirect("drive_root")


def get_user_folder_size(user_folder_path):
    """Calculer la taille totale des fichiers dans le dossier de l'utilisateur."""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(user_folder_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size
