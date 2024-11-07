import os
from django.shortcuts import redirect
from drive.models import File, Folder, Thumbnail
from django.conf import settings
import shutil

def delete_file(request):
    if request.method == 'POST':
        print("delete file")
        id = request.POST.get('file_id')
        print(f"folder : {id}")
        
        file = File.objects.get(id=id, owner=request.user)
        print(f'file : {file}')
        
        path = request.POST.get("current_path")
        print(f"path : {path}")
        
        base_dir = os.path.join(settings.MEDIA_ROOT, request.user.username)
        print(f'base dir : {base_dir}')
        
        file_path = os.path.join(base_dir, path)
        file_path = os.path.join(file_path, file.name)
        
        parent_folder = file.parent
        
        print(f"file path : {file_path}")
        if os.path.exists(file_path):
            os.remove(file_path)
            if parent_folder.number_of_elements > 0:
                parent_folder.number_of_elements -= 1
            
            try:
                thumbnail = Thumbnail.objects.get(file=file)
                os.remove(os.path.join(settings.BASE_DIR, 'thumbnails', thumbnail.image))
                
                thumbnail.delete()  
            except Thumbnail.DoesNotExist or os.error:
                pass
            
            file.delete()
            parent_folder.save()
        
        if path == '':
            return redirect('drive')
    
    return redirect('drive', path=path)

def delete_folder(request):
    if request.method == 'POST':
        print("delete folder")
        id = request.POST.get('folder_id')
        print(f"folder : {id}")
        
        folder = Folder.objects.get(id=id, owner=request.user)
        print(f'folder : {folder}')
        
        path = request.POST.get("current_path")
        print(f"path : {path}")
        
        base_dir = os.path.join(settings.MEDIA_ROOT, request.user.username)
        print(f'base dir : {base_dir}')
        
        folder_path = os.path.join(base_dir, path)
        folder_path = os.path.join(folder_path, folder.name)
        
        # file_path = os.path.join(file_path, file.name)
        print(f"folder path : {folder_path}")
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
            folder.delete()
        
        if path == '':
            return redirect('drive')
    
    return redirect('drive', path=path)