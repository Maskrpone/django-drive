import os
from django.shortcuts import redirect
from django.conf import settings

def create_folder(request):
    if request.method == "POST":
        folder_name = request.POST.get("folder_name")
        if folder_name:
            path = request.POST.get("current_path")
            if path:
               base_dir = os.path.join(settings.MEDIA_ROOT, "Hippolyte")
               folder_path = os.path.join(base_dir, path)
            else:
               folder_path = os.path.join(settings.MEDIA_ROOT, "Hippolyte")
            
            full_path = os.path.join(folder_path, folder_name)
            
            os.makedirs(full_path, exist_ok=True)
            
            if path:
                return redirect("drive", path=path)
    return redirect("drive_root")