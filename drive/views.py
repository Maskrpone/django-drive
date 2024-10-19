from django.shortcuts import render
import os


# Create your views here.
def home(request, path="", username="maskrpone"):

    base_path = os.path.join("storage", username)

    # Construire le chemin complet en combinant le chemin de base avec le sous-dossier
    full_path = os.path.join(base_path, path)

    # Vérifier si le répertoire existe
    if not os.path.exists(full_path):
        files_and_dirs = []
    else:
        # Liste des fichiers et dossiers
        files_and_dirs = os.listdir(full_path)

    # Préparer une liste où chaque élément est un dictionnaire contenant le nom et le type (fichier/dossier)
    items = []
    for item in files_and_dirs:
        item_full_path = os.path.join(full_path, item)
        if os.path.isdir(item_full_path):
            items.append({"name": item, "is_dir": True})  # C'est un dossier
        else:
            items.append({"name": item, "is_dir": False})  # C'est un fichier

    context = {
        "items": items,  # Passe la liste des items avec leur type (fichier/dossier)
        "current_path": path,  # Le chemin relatif actuel
        "username": username,
        "is_root": path == "",  # Indique si on est à la racine
    }
    return render(request, "drive/home.html", context)
