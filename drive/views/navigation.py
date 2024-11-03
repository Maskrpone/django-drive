import os
from django.conf import settings
from django.http import Http404
from django.shortcuts import render, redirect
from ..forms import FileUploadForm
from ..models import Folder

def home(request, path=""):
    
    if not request.session.session_key:
        return redirect('login_view')
    
    base_dir = os.path.join(settings.MEDIA_ROOT, request.user.username)
    folder_path = os.path.join(base_dir, path)
    print(f'accessing to {folder_path}')
    
    if not os.path.exists(folder_path):
        raise Http404("Dossier non trouvé")
    
    folders = [name for name in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, name))]
    files = [name for name in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, name))]
    breadcrumbs = get_breadcrumbs(path)
    
    return render(request, "drive/path.html", {
        'folders': folders,
        'files': files,
        'current_path': f'{path}',
        'breadcrumbs': breadcrumbs,
        'form': FileUploadForm
    })
    
    
def get_breadcrumbs(path):
    path = path.strip().split('/')
    breadcrumbs = {}
    accumulated_path = ""
    for part in path:
        accumulated_path = f'{os.path.join(accumulated_path, part)}/'
        breadcrumbs[part] = accumulated_path
    
    return breadcrumbs
