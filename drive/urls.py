from django.urls import path
from . import views

urlpatterns = [
    path("<str:username>/", views.home, name="drive"),
    path('folder/<str:username>/<path:path>/', views.folder_contents, name='folder_contents'),
    path('upload/<str:username>/', views.upload, name='upload_root'),
    path('upload/<str:username>/<path:path>', views.upload, name='upload')
]
