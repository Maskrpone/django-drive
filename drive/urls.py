from django.urls import path
from .views import navigation, folder, upload

urlpatterns = [
    path("upload/", upload.upload_file, name="upload_file"),
    path("create_folder/",  folder.create_folder, name="create_folder"),
    path("", navigation.home, {'path': ''}, name="drive_root"),
    path("<path:path>", navigation.home, name="drive"),
]