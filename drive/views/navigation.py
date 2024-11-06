import os
from django.conf import settings
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from ..forms import FileUploadForm
from ..models import Folder, File, Thumbnail
from drive.views.folder import get_parent_folder

def home(request: HttpRequest, path:str="") -> HttpResponse:
    """This is the base view for navigating through the drive."""
    
    # We check if there is an active session 
    if not request.session.session_key:
        return redirect('login_view')
    
    # We get the current path
    base_dir = os.path.join(settings.MEDIA_ROOT, request.user.username)
    folder_path = os.path.join(base_dir, path)
    
    # If we can't find the specified path, we raise a 404
    if not os.path.exists(folder_path):
        raise Http404("Dossier non trouvé")
    
    # we will need it later
    parent_id = get_parent_folder(folder_path, request.user)
    
    # We list the content of the current folder 
    folders_name = [name for name in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, name))]

    folders = []  
    for folder in folders_name:
        print(f"parent id {parent_id}")
        actual_folder = Folder.objects.get(name=folder, parent=parent_id, owner=request.user)
        
        folders.append({"name": folder, "elts": actual_folder.number_of_elements, "last_updated": actual_folder.last_updated})
    
    files_name = [name for name in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, name))]
    
    files = []
    for file in files_name:
        actual_file = File.objects.get(name=file, parent=parent_id, owner=request.user)
        if len(Thumbnail.objects.filter(file=actual_file)) == 1:
            thumbnail_name = Thumbnail.objects.get(file=actual_file).image
        else:
            thumbnail_name = None
        
        if thumbnail_name != None:
            thumbnail = f"{settings.THUMBNAILS_URL}{thumbnail_name}"
            print(f'Path for thumbnail : {thumbnail}')
        else:
            thumbnail = None
        
        files.append({"name": file, "size": actual_file.size, "date": actual_file.uploaded_at, "thumbnail": thumbnail }) 
    
    breadcrumbs = get_breadcrumbs(path)
    
    return render(request, "drive/path.html", {
        'folders': folders,
        'files': files,
        'current_path': f'{path}',
        'breadcrumbs': breadcrumbs,
        'form': FileUploadForm
    })
    
    
def get_breadcrumbs(path: str) -> dict:
    """Used to get a dictionnary with links to all the nested folders of the current path"""
    path = path.strip('/').split('/')
    breadcrumbs = {}
    accumulated_path = ""
    for part in path:
        accumulated_path = f'{os.path.join(accumulated_path, part)}/'
        breadcrumbs[part] = accumulated_path
    
    return breadcrumbs
