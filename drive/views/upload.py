import os
from django.shortcuts import redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseBadRequest
from ..forms import FileUploadForm

def upload_file(request):
    if request.method == "POST":
        form = FileUploadForm(request.POST, request.FILES)
        path = request.POST.get("current_path")
        if path:
           base_dir = os.path.join(settings.MEDIA_ROOT, "Hippolyte")
           folder_path = os.path.join(base_dir, path)
        else:
           folder_path = os.path.join(settings.MEDIA_ROOT, "Hippolyte")
        
        os.makedirs(folder_path, exist_ok=True)
        
        if form.is_valid():
            uploaded_file = request.FILES["file"]
            if uploaded_file.size > 40 * 1024 * 1024:
                return HttpResponseBadRequest("File size exceeds 40MB limit")
            fs = FileSystemStorage(location=folder_path)
            fs.save(uploaded_file.name, uploaded_file)
        else:
            return HttpResponseBadRequest("Invalid form")
        if path:
            return redirect("drive", path=path)
    return redirect("drive_root")