import os
import matplotlib.pyplot as plt

def get_folder_size_by_format(folder_path):
    """
    Parcourt un dossier et calcule la taille totale des fichiers par format.

    :param folder_path: Chemin du dossier à analyser
    :return: Un dictionnaire avec l'extension de fichier comme clé et la taille totale en octets comme valeur
    """
    size_by_format = {}

    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            # Obtenir l'extension et la taille du fichier
            _, extension = os.path.splitext(file)
            extension = extension.lower()  # Mettre en minuscules pour éviter les doublons comme ".JPG" et ".jpg"
            file_size = os.path.getsize(file_path)
            
            # Ajouter la taille au format correspondant
            if extension in size_by_format:
                size_by_format[extension] += file_size
            else:
                size_by_format[extension] = file_size

    # Convertir les tailles en Mo
    size_by_format = {ext: round(size / (1024 * 1024), 2) for ext, size in size_by_format.items()}
    return size_by_format

def generate_storage_chart(data):
    """
    Génère un graphique à secteurs représentant la répartition de l'espace par format et l'affiche.

    :param data: Un dictionnaire contenant le format des fichiers et leur taille en Mo
    """
    labels = list(data.keys())
    sizes = list(data.values())

    # Création du graphique
    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')  # Assure un cercle
    plt.title("Répartition de l'espace par format")
    
    # Enregistrer et afficher l'image
    plt.savefig("storage_chart.png")
    print("Graphique sauvegardé sous 'storage_chart.png'")
    plt.show()

# Utiliser le dossier spécifié
folder_path = "storage/Hippolyte"
data = get_folder_size_by_format(folder_path)
generate_storage_chart(data)
