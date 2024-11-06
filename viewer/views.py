import os
from django.conf import settings
from django.shortcuts import render
from drive.models import File


# Create your views here.
def view_doc(request, id:int):
    try:
        folder_infos = []
        current_file = File.objects.get(id=id, owner=request.user)
        file = current_file
        print(f"current file : {current_file}")
        while current_file.parent is not None:
            folder_infos.append(current_file.parent.name)
            current_file = current_file.parent
    except File.DoesNotExist:
        print("File does not exist")
        
    file_path = ""
    for folder in reversed(folder_infos):
        file_path = os.path.join(file_path, folder)
    
    print(f"file_path : {file_path}")
    full_path = os.path.join(settings.MEDIA_URL, file_path)
    print(f"full_path : {full_path}")
    
    path = os.path.join(full_path, file.name)
    
    if file.file_type.startswith('image'):
        type = 'image'
    elif file.file_type.split('/')[-1] == 'pdf':
        type = 'pdf'
    elif file.file_type.startswith('video'):
        type = 'video'
    else:
        type = 'unknown'
    
    
    return render(request, 'viewer/viewer.html', {'file_location': path, 'metadata': file, 'type': type })