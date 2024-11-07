import os
from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth.models import User
from ..models import Folder
from django.http import HttpRequest, HttpResponse

def create_folder(request: HttpRequest) -> HttpResponse:
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
            print(f'test : {folder_name}')
            parent = get_parent_folder(folder_path, request.user)
            new_folder = Folder.objects.create(name=folder_name, owner=request.user, parent=parent)
            print(f'new folder : {new_folder}')
            new_folder.save()
            os.makedirs(full_path, exist_ok=True)
            
            if path:
                return redirect("drive", path=path)
    return redirect("drive_root")

def get_parent_folder(folder_path: str, owner: User) -> Folder:
    """This function return with the ID of the parent folder

    Args:
        folder_path (str): This is supposed to be the path to the folder for which we are looking the ID
        owner (User): User object

    Returns:
        Folder: This is the ID of the parent folder
    """
    # Construct relative path
    folder_path = folder_path.split('storage' + os.sep, 1)[-1]
    folder_path = os.path.normpath(folder_path)
    folder_list = folder_path.split(os.sep)
    print(f'folder list : {folder_list}')
    
    base_folder = Folder.objects.get(name=owner.username, owner=owner, parent=None)
    current_parent = base_folder
    for folder_name in folder_list[1:]:
        current_parent = Folder.objects.get(name=folder_name, owner=owner, parent=current_parent)
    
    return current_parent