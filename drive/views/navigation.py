import os
import mimetypes
from django.conf import settings
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from ..forms import FileUploadForm
from ..models import Folder, File, Thumbnail
from drive.views.folder import get_parent_folder
from drive.views.upload import create_thumbnail

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
        return redirect('drive_root')
    
    # we will need it later
    parent_id = get_parent_folder(folder_path, request.user)
    
    # We list the content of the current folder 
    folders_name = [name for name in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, name))]
    
    folders = []  
    for folder in folders_name:
        print(f"Trying for folder {folder}")
        print(f"parent id {parent_id.id}")
        try: 
            actual_folder = Folder.objects.get(name=folder, parent=parent_id, owner=request.user)
        except Folder.DoesNotExist:
            actual_folder = Folder.objects.create(name=folder, parent=parent_id, owner=request.user)
            continue
        
        folders.append({"name": folder, "elts": actual_folder.number_of_elements, "last_updated": actual_folder.last_updated, "id": actual_folder.id})
    
    files_name = [name for name in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, name))]
    
    files = []
    for file in files_name:
        try:
            actual_file = File.objects.get(name=file, parent=parent_id, owner=request.user)
        except File.DoesNotExist:
            type,_ = mimetypes.guess_type(file)
            actual_file = File.objects.create(name=file, parent=parent_id, owner=request.user, size=os.path.getsize(os.path.join(folder_path, file)), file_type=type)
            continue
        
        if len(Thumbnail.objects.filter(file=actual_file)) == 1:
            thumbnail_name = Thumbnail.objects.get(file=actual_file).image
        else:
            thumbnail_name = None
        
        if thumbnail_name != None:
            thumbnail = f"{settings.THUMBNAILS_URL}{thumbnail_name}"
            print(f'Path for thumbnail : {thumbnail}')
        else:
            thumbnail = None
        
        if actual_file.file_type != None:
            type = actual_file.file_type.split('/')[-1]
        else:
            type = "unknown"
        
        files.append({"name": file, "size": actual_file.size, "date": actual_file.uploaded_at, "thumbnail": thumbnail, "id": actual_file.id, "type": type }) 
    
    breadcrumbs = get_breadcrumbs(path)
    
    return render(request, "drive/path.html", {
        'folders': folders,
        'files': files,
        'current_path': f'{path}',
        'breadcrumbs': breadcrumbs,
        'form': FileUploadForm,
    })
    
    
def get_breadcrumbs(path: str) -> list:
    """Used to get a dictionnary with links to all the nested folders of the current path"""
    path = path.strip('/').split('/')
    breadcrumbs = []
    accumulated_path = ""
    for part in path:
        accumulated_path = f'{os.path.join(accumulated_path, part)}/'
        breadcrumbs.append((part, accumulated_path))
    
    return breadcrumbs