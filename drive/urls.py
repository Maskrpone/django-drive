from django.urls import path
from .views import navigation, folder, upload, reader, delete
from .views.metadata_view import list_user_files_with_metadata


urlpatterns = [
    path("upload/", upload.upload_file, name="upload_file"),
    path("create_folder/",  folder.create_folder, name="create_folder"),
    path("read_file/<path:path>", reader.file_reader, name="read_file"),
    path("delete_file/", delete.delete_file, name="delete_file"),
    path("delete_folder/", delete.delete_folder, name="delete_folder"),
    path("", navigation.home, {'path': ''}, name="drive_root"),
    path("<path:path>", navigation.home, name="drive"),
    path('user_files/<str:username>/', list_user_files_with_metadata, name='user_files_metadata'),
]