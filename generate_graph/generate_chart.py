import os
import matplotlib.pyplot as plt
from datetime import datetime

# Limite totale en Mo
TOTAL_STORAGE_MB = 100

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

    # Convertir les tailles en Mo
    size_by_format = {ext: round(size / (1024 * 1024), 2) for ext, size in size_by_format.items()}
    return size_by_format

def generate_combined_chart(folder_path):
    # Préparation des données pour le premier graphique (Répartition de l'espace par format)
    data = get_folder_size_by_format(folder_path)
    labels_format = list(data.keys())
    sizes_format = list(data.values())

    # Calcul de l'espace utilisé et restant pour le second graphique
    total_used_mb = sum(data.values())
    remaining_mb = max(TOTAL_STORAGE_MB - total_used_mb, 0)

    labels_storage = ['Utilisé', 'Disponible']
    sizes_storage = [total_used_mb, remaining_mb]

    # Création d'une figure avec deux sous-graphiques
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

    # Premier graphique : Répartition de l'espace par format
    ax1.pie(sizes_format, labels=labels_format, autopct='%1.1f%%', startangle=140)
    ax1.axis('equal')  # Assure un cercle
    ax1.set_title("Répartition de l'espace par format")

    # Second graphique : Espace utilisé vs espace restant
    ax2.pie(sizes_storage, labels=labels_storage, autopct='%1.1f%%', startangle=140, colors=["red", "green"])
    ax2.axis('equal')
    ax2.set_title(f"Utilisation du stockage sur {TOTAL_STORAGE_MB} Mo")

    # Sauvegarder l'image combinée
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_dir = os.path.join("generate_graph", "static", "charts")
    os.makedirs(save_dir, exist_ok=True)
    filename = f"combined_chart_{timestamp}.png"
    filepath = os.path.join(save_dir, filename)
    
    plt.savefig(filepath)
    print(f"Graphiques combinés sauvegardés sous '{filepath}'")
    plt.show()

# Utiliser le dossier pour les données
folder_path = "storage/hippolyte"
generate_combined_chart(folder_path)
