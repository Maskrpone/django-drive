# Generated by Django 5.1.2 on 2024-10-27 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drive', '0002_file_folder_delete_document_file_folder'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='folder',
            name='owner',
        ),
        migrations.AlterField(
            model_name='file',
            name='file',
            field=models.FileField(upload_to='files/'),
        ),
    ]
