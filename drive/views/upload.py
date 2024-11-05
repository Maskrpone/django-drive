import os
from django.shortcuts import redirect, get_list_or_404
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.http import HttpResponseBadRequest, HttpResponse, HttpRequest
from ..forms import FileUploadForm
from drive.models import File
from drive.views.folder import get_parent_folder

MAX_STORAGE_LIMIT = 100 * 1024 * 1024  # 100 MB

def get_user_folder_size(user: User) -> int:
    """Calculer la taille totale des fichiers dans le dossier de l'utilisateur."""
    
    list_files = File.objects.filter(owner=user.id) # We retrieve all the files owned by a specific user
    
    # We sum their sizes
    actual_used_capacity = 0
    for file in list_files:
        actual_used_capacity += file.size
    
    print(f"actual used space for {user} : {actual_used_capacity}")
    return actual_used_capacity 

def upload_file(request: HttpRequest) -> HttpResponse:
    """This is the view for file uploading"""
    if request.method == "POST":
        print(f"test")
        form = FileUploadForm(request.POST, request.FILES) # We get the form to check if it is valid
        path = request.POST.get("current_path") # We get the current path (where we want to place the uploaded file)
        base_dir = os.path.join(settings.MEDIA_ROOT, request.user.username) # We form the root directory of the actual user
        
        print(f'base_dir : {base_dir}')
        
        # If our path is different from the root, we constitute it
        if path:
           folder_path = os.path.join(base_dir, path)
        else:
           folder_path = base_dir
        
        print(f'path: {path}')
        
        os.makedirs(folder_path, exist_ok=True) # ensures that our target folder exists
        
        # We must make sure that our form is valid before trying to upload the file
        if form.is_valid():
            uploaded_file = request.FILES["file"] # We get the file
            print(f"uploaded file : {uploaded_file.name}")
            # We check if the file is larger than 40 Mo
            if uploaded_file.size > 40 * 1024 * 1024:
                return HttpResponseBadRequest("File size exceeds 40MB limit")
            print(f'passed the size')
            # We check if the allocated size (100 Mo) for a user is exceeded or not 
            user_used_capacity = get_user_folder_size(request.user)
            if user_used_capacity + uploaded_file.size > MAX_STORAGE_LIMIT:
                return HttpResponseBadRequest("Storage limit of 100MB exceeded")
            
            # Prepare metadata for registration into the database
            parent_folder = get_parent_folder(folder_path, request.user)
            size = uploaded_file.size / 1024 # Get the size in Ko
            
            fs = FileSystemStorage(location=folder_path)
            fs.save(uploaded_file.name, uploaded_file)
            
            # Database registration
            File.objects.create(name=uploaded_file.name, size=size, owner=request.user, parent_id=parent_folder.id)
            
        else:
            return HttpResponseBadRequest("Invalid form")
        
        # Redirections are the same, but for code clarity we are making the distinction between root or path 
        if path:
            return redirect("drive", path=path)
    return redirect("drive_root")



