from django.urls import path
from .views import view_doc
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("<int:id>/", view_doc, name="file_viewer" )
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
