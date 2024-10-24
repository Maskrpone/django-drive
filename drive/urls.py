from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path('folder/<str:username>/<path:path>/', views.folder_contents, name='folder_contents'),
]
