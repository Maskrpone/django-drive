import os
from django.shortcuts import render
from datetime import datetime

def list_user_files_with_metadata(request, username):
    folder_path = f'storage/{username}'  # Dossier de l'utilisateur
    files_data = []

    if os.path.exists(folder_path):
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):  # Vérifie si c'est un fichier
                # Récupère les métadonnées du fichier
                file_info = {
                    'name': filename,
                    'size': os.path.getsize(file_path),  # Taille en octets
                    'last_modified': datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S'),  # Dernière modification
                    'created': datetime.fromtimestamp(os.path.getctime(file_path)).strftime('%Y-%m-%d %H:%M:%S'),  # Date de création
                    'type': os.path.splitext(filename)[1].replace('.', '').upper()  # Extension du fichier
                }
                files_data.append(file_info)
    else:
        # Le dossier n'existe pas (par exemple, si l'utilisateur n'a pas de fichiers)
        files_data = None

    # Passe les données au template
    return render(request, 'file_metadata.html', {'files_data': files_data, 'username': username})
