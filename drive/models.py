from django.db import models
from django.contrib.auth.models import User

class Folder(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', null=True, blank=True, related_name="subfolder", on_delete=models.CASCADE)
    owner = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    number_of_elements = models.PositiveIntegerField(null=False, default=0)
    last_updated = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.name
    
    def path(self):
        if self.parent:
            return f'{self.parent.path()}/{self.name}'

class File(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey(Folder, null=True, blank=True, related_name="parent_folder", on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    size = models.IntegerField(null=False, default=0)
    owner = models.ForeignKey(User, null=True, blank=False, related_name="owner_files", on_delete=models.CASCADE)
    file_type = models.CharField(max_length=10, null=True)
    
    def __str__(self):
        return self.name