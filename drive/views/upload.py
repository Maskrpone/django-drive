import os
import mimetypes
import pymupdf
from PIL import Image
from pdf2image import convert_from_path
from io import BytesIO
from django.shortcuts import redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from django.contrib.auth.models import User
from django.http import HttpResponseBadRequest, HttpResponse, HttpRequest
from ..forms import FileUploadForm
from drive.models import File, Thumbnail
from drive.views.folder import get_parent_folder
from django.utils import timezone
import uuid
from django.contrib.auth.decorators import login_required

MAX_STORAGE_LIMIT = 100 * 1024 * 1024  # 100 MB

@login_required
def get_user_folder_size(user: User) -> int:
    """Calculer la taille totale des fichiers dans le dossier de l'utilisateur."""
    
    list_files = File.objects.filter(owner=user.id) # We retrieve all the files owned by a specific user
    
    # We sum their sizes
    actual_used_capacity = 0
    for file in list_files:
        actual_used_capacity += file.size
    
    print(f"actual used space for {user} : {actual_used_capacity}")
    return actual_used_capacity 

@login_required
def upload_file(request: HttpRequest) -> HttpResponse:
    """This is the view for file uploading"""
    if request.method == "POST":
        print(f"test")
        form = FileUploadForm(request.POST, request.FILES) # We get the form to check if it is valid
        path = request.POST.get("current_path") # We get the current path (where we want to place the uploaded file)
        base_dir = os.path.join(settings.MEDIA_ROOT, request.user.username) # We form the root directory of the actual user
        print(f"base dir : {base_dir}")
        # If our path is different from the root, we constitute it
        if path:
           folder_path = os.path.join(base_dir, path)
        else:
           folder_path = base_dir
        print(f"folder path : {folder_path}")
        os.makedirs(folder_path, exist_ok=True) # ensures that our target folder exists
        
        # We must make sure that our form is valid before trying to upload the file
        if form.is_valid():
            uploaded_file = request.FILES["file"] # We get the file
            print(f"uploaded file : {uploaded_file.name}")
            # We check if the file is larger than 40 Mo
            if uploaded_file.size > 40 * 1024 * 1024:
                return HttpResponseBadRequest("File size exceeds 40MB limit")
            print(f'passed the size')
            
            # We check if the allocated size (100 Mo) for a user is exceeded or not 
            user_used_capacity = get_user_folder_size(request.user)
            if user_used_capacity + uploaded_file.size > MAX_STORAGE_LIMIT:
                return HttpResponseBadRequest("Storage limit of 100MB exceeded")
            
            all_files = [name for name in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, name))]
            
            while uploaded_file.name in all_files:
                uploaded_file.name = f'copy_{uploaded_file.name}'
                all_files = [name for name in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, name))]
            
            print(f'new name : {uploaded_file.name}')
            # Prepare metadata for registration into the database
            parent_folder = get_parent_folder(folder_path, request.user)
            size = uploaded_file.size / 1024 # Get the size in Ko
            
            fs = FileSystemStorage(location=folder_path)
            fs.save(uploaded_file.name, uploaded_file)
            
            # Database registration
            file_type,_ = mimetypes.guess_type(uploaded_file.name)
            if file_type is None:
                file_type = 'unknown'
            item = File.objects.create(name=uploaded_file.name, size=size, owner=request.user, parent_id=parent_folder.id, file_type=file_type)
            
            create_thumbnail(uploaded_file, item, request.user, folder_path)
            
            parent_folder.number_of_elements += 1
            parent_folder.last_updated = timezone.now().date()
            parent_folder.save()
            
        else:
            return HttpResponseBadRequest("Invalid form")
        
        # Redirections are the same, but for code clarity we are making the distinction between root or path 
        if path:
            return redirect("drive", path=path)
    return redirect("drive_root")


def get_user_folder_size(user: User) -> int:
    """Calculer la taille totale des fichiers dans le dossier de l'utilisateur."""
    
    list_files = File.objects.filter(owner=user.id) # We retrieve all the files owned by a specific user
    
    # We sum their sizes
    actual_used_capacity = 0
    for file in list_files:
        actual_used_capacity += file.size
    
    print(f"actual used space for {user} : {actual_used_capacity}")
    return actual_used_capacity

def create_thumbnail(uploaded_file, file_db: File, user: User, folder_path: str):
    print(f'{file_db.file_type.split("/")[-1]}')
    if file_db.file_type.split("/")[0] == "image":
        image = Image.open(uploaded_file)
        image.thumbnail((150,150))
        thumb_IO = BytesIO()
        image.save(thumb_IO, format=image.format)

        random_name = f'thumb_{uuid.uuid4().hex}_{uploaded_file.name}'
        print(f'random name : {random_name}')
        
        while len(Thumbnail.objects.filter(image=random_name)) != 0:
            random_name = f'thumb_{uuid.uuid4().hex}_{uploaded_file.name}'
            
        fs = FileSystemStorage(location=settings.THUMBNAILS_ROOT)
        fs.save(random_name, ContentFile(thumb_IO.getvalue()))
        
        thumbnail = Thumbnail.objects.create(file=file_db, image=random_name)
        thumbnail.save()
        return
    
    if file_db.file_type.split('/')[-1] == "pdf":
        
        pdf_path = os.path.join(folder_path, uploaded_file.name)
        print(f'folder path : {pdf_path}')
        
        pdf = pymupdf.open(pdf_path)
        
        page = pdf.load_page(0)
        
        image = page.get_pixmap()
        
        image = Image.frombytes("RGB", [image.width, image.height], image.samples)
        image.thumbnail((150, 150))

        thumb_IO = BytesIO()
        image.save(thumb_IO, format='PNG')

        random_name = f'thumb_{uuid.uuid4().hex}_{uploaded_file.name.split('.')[0]}.png'
        print(f'random name : {random_name}')
        
        while len(Thumbnail.objects.filter(image=random_name)) != 0:
            random_name = f'thumb_{uuid.uuid4().hex}_{uploaded_file.name.split('.')[0]}.png'
            
        fs = FileSystemStorage(location=settings.THUMBNAILS_ROOT)
        fs.save(random_name, ContentFile(thumb_IO.getvalue()))
        
        thumbnail = Thumbnail.objects.create(file=file_db, image=random_name)
        thumbnail.save()
        return
        