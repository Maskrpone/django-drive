from django.urls import path
from .views import navigation

urlpatterns = [
    path("", navigation.home, {'path': ''}, name="drive_root"),
    path("<path:path>", navigation.home, name="drive"),
]