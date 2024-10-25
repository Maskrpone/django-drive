from django.urls import path
from .views import navigation, upload

urlpatterns = [
    path("<str:username>/", navigation.home, name="drive"),
    path('folder/<str:username>/<path:path>/', navigation.folder_contents, name='folder_contents'),
    path('upload/<str:username>/', upload.upload, name='upload_root'),
    path('upload/<str:username>/<path:path>', upload.upload, name='upload')
]
