# Generated by Django 5.1.2 on 2024-11-03 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drive', '0006_alter_folder_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='folder',
        ),
        migrations.AlterField(
            model_name='file',
            name='file',
            field=models.FileField(upload_to='storage/'),
        ),
    ]
