import os
import matplotlib.pyplot as plt
from datetime import datetime

def get_folder_size_by_format(folder_path):
    size_by_format = {}

    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            _, extension = os.path.splitext(file)
            extension = extension.lower()
            file_size = os.path.getsize(file_path)
            
            if extension in size_by_format:
                size_by_format[extension] += file_size
            else:
                size_by_format[extension] = file_size

    size_by_format = {ext: round(size / (1024 * 1024), 2) for ext, size in size_by_format.items()}
    return size_by_format

def generate_storage_chart(data):
    labels = list(data.keys())
    sizes = list(data.values())

    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.title("Répartition de l'espace par format")
    
    # Définir le dossier de sauvegarde
    save_dir = os.path.join("generate_graph", "static", "charts")
    os.makedirs(save_dir, exist_ok=True)  # Créer le dossier s'il n'existe pas

    # Générer un nom de fichier unique avec horodatage
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"storage_chart_{timestamp}.png"
    filepath = os.path.join(save_dir, filename)
    
    # Sauvegarder le graphique
    plt.savefig(filepath)
    print(f"Graphique sauvegardé sous '{filepath}'")
    plt.show()

# Utiliser le dossier spécifié pour les données
folder_path = "storage/hippolyte"
data = get_folder_size_by_format(folder_path)
generate_storage_chart(data)
