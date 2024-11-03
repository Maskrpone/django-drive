import os
from django.shortcuts import redirect, get_object_or_404
from django.conf import settings
from ..models import Folder

def create_folder(request):
    if request.method == "POST":
        folder_name = request.POST.get("folder_name")
        
        base_dir = os.path.join(settings.MEDIA_ROOT, request.user.username)
        
        if folder_name:
            path = request.POST.get("current_path")
            if path:
               folder_path = os.path.join(base_dir, path)
            else:
               folder_path = base_dir
            
            full_path = os.path.join(folder_path, folder_name)
            
            if os.path.exists(full_path):
                return redirect("drive", path=path if path else "")
            
            new_folder = Folder.objects.create(name=folder_name, owner=request.user)
            print(f'new folder : {new_folder}')
            new_folder.save()
            os.makedirs(full_path, exist_ok=True)
            
            if path:
                return redirect("drive", path=path)
    return redirect("drive_root")