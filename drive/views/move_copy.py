import os
import shutil
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.urls import reverse

def move_file_or_folder(request):
    if request.method == "POST":
        source_path = request.POST.get("source_path")
        destination_path = request.POST.get("destination_path")

        if source_path and destination_path:
            try:
                shutil.move(source_path, destination_path)
                return JsonResponse({"status": "success", "message": "Déplacé avec succès"})
            except Exception as e:
                return JsonResponse({"status": "error", "message": str(e)})

    return JsonResponse({"status": "error", "message": "Chemins non valides"})

def copy_file_or_folder(request):
    if request.method == "POST":
        source_path = request.POST.get("source_path")
        destination_path = request.POST.get("destination_path")

        if source_path and destination_path:
            try:
                if os.path.isfile(source_path):
                    shutil.copy2(source_path, destination_path)
                else:
                    shutil.copytree(source_path, os.path.join(destination_path, os.path.basename(source_path)))
                return JsonResponse({"status": "success", "message": "Copié avec succès"})
            except Exception as e:
                return JsonResponse({"status": "error", "message": str(e)})

    return JsonResponse({"status": "error", "message": "Chemins non valides"})

def delete_file_or_folder(request):
    if request.method == "POST":
        filepath = request.POST.get("filepath")

        if filepath and os.path.exists(filepath):
            try:
                # Vérifier si le chemin est un fichier ou un dossier
                if os.path.isfile(filepath):
                    os.remove(filepath)  # Supprimer le fichier
                elif os.path.isdir(filepath):
                    shutil.rmtree(filepath)  # Supprimer le dossier et son contenu
                return JsonResponse({"status": "success", "message": "Supprimé avec succès."})
            except Exception as e:
                return JsonResponse({"status": "error", "message": f"Erreur lors de la suppression: {e}"})
        else:
            return JsonResponse({"status": "error", "message": "Chemin non valide ou introuvable."})
    return JsonResponse({"status": "error", "message": "Requête non valide."})
