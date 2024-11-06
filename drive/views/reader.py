from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from drive.models import File
from drive.views.folder import get_parent_folder

@login_required
def file_reader(request, file_path: str):
    file_name = file_path.split('/')[-1]
    parent_path = file_path.replace(file_name, "")
    parent_id = get_parent_folder(parent_path, request.user)
    file_data = File.objects.get(file_name, parent_id, request.user)
    return render(request, "drive/file_reader.html", {
        "file": file_data,
        "url": file_path,
    })