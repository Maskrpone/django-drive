import os
from django.shortcuts import get_list_or_404
import matplotlib.pyplot as plt
from datetime import datetime
from io import BytesIO
import base64

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

    size_by_format = {ext: round(size / (1024 * 1024), 2) for ext, size in size_by_format.items()}
    return size_by_format

def generate_combined_chart(folder_path):
    data = get_folder_size_by_format(folder_path)
    labels_format = list(data.keys())
    sizes_format = list(data.values())

    total_used_mb = sum(data.values())
    remaining_mb = max(TOTAL_STORAGE_MB - total_used_mb, 0)

    labels_storage = ['Utilisé', 'Disponible']
    sizes_storage = [total_used_mb, remaining_mb]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

    ax1.pie(sizes_format, labels=labels_format, autopct='%1.1f%%', startangle=140)
    ax1.axis('equal')
    ax1.set_title("Répartition de l'espace par format")

    ax2.pie(sizes_storage, labels=labels_storage, autopct='%1.1f%%', startangle=140, colors=["red", "green"])
    ax2.axis('equal')
    ax2.set_title(f"Utilisation du stockage sur {TOTAL_STORAGE_MB} Mo")

    buf = BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)

    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    return image_base64
