from django.db import models

class Folder(models.Model):
    folder_name = models.CharField(max_length=255)
    parent_folder = models.ForeignKey("self", on_delete=models.CASCADE, null=True)
    # owner = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    owner = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
class File(models.Model):
    file_name = models.CharField(max_length=255)
    parent_folder = models.ForeignKey(Folder, on_delete=models.CASCADE)
    file_size = models.IntegerField()
    owner = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    file_type = models.CharField(max_length=50)