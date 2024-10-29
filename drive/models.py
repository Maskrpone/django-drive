from django.db import models
from django.contrib.auth.models import User

class Folder(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', null=True, blank=True, related_name="subfolder", on_delete=models.CASCADE)
    owner = models.ForeignKey(User, null=True, blank=False, related_name="owner_folders", on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
    def path(self):
        if self.parent:
            return f'{self.parent.path()}/{self.name}'

class File(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to="files/")
    folder = models.ForeignKey(Folder, related_name='files', on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    size = models.IntegerField(default=0)
    owner = models.ForeignKey(User, null=True, blank=False, related_name="owner_files", on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name