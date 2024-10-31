import os
import matplotlib.pyplot as plt

# Dossier de l'utilisateur
USER_FOLDER = os.path.join("storage", "Hippolyte")
print(f"User folder path: {USER_FOLDER}")

if not os.path.exists(USER_FOLDER):
    print(f"Error: The user folder {USER_FOLDER} does not exist.")

# Définitions des extensions par type
FILE_TYPES = {
    "images": [".jpg", ".jpeg", ".png", ".gif"],
    "videos": [".mp4", ".mov", ".avi"],
    "documents": [".pdf", ".docx", ".txt", ".xlsx"],
    "audio": [".mp3", ".wav"],
}

with open("static/charts/test.txt", "w") as f:
    f.write("Test file creation.")


def calculate_storage_by_format(user_folder):
    """Calculer l'espace occupé par chaque type de fichier."""
    format_sizes = {category: 0 for category in FILE_TYPES.keys()}
    for dirpath, dirnames, filenames in os.walk(user_folder):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            file_size = os.path.getsize(file_path)
            file_extension = os.path.splitext(filename)[1].lower()
            
            # Débogage : afficher le fichier trouvé et sa taille
            print(f"Found file: {file_path}, Size: {file_size}, Extension: {file_extension}")

            # Attribution de la taille en fonction du type
            for category, extensions in FILE_TYPES.items():
                if file_extension in extensions:
                    format_sizes[category] += file_size
                    break
    return format_sizes

def generate_chart(user_folder):
    """Générer un graphique de répartition par format."""
    # Calculer les tailles de chaque format
    format_sizes = calculate_storage_by_format(user_folder)
    
    # Débogage : Afficher les tailles calculées
    print("Taille par format:", format_sizes)

    # Filtrer les formats qui ont une taille > 0
    labels = [category for category, size in format_sizes.items() if size > 0]
    sizes = [size for size in format_sizes.values() if size > 0]

    if not sizes:  # Vérifier si aucune taille n'est trouvée
        print("Aucune taille trouvée pour générer le graphique.")
        return None  # Sortir de la fonction si aucune taille n'est trouvée

    # Création du graphique
    plt.figure(figsize=(8, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title("Répartition de l'espace de stockage par format")
    
    # Sauvegarder le graphique dans un fichier
    chart_path = os.path.join("static", "charts", "format_distribution.png")
    plt.savefig(chart_path)
    print(f"Chemin du graphique : {chart_path}")
    plt.close()
    return chart_path

# Appeler la fonction pour générer le graphique
if __name__ == "__main__":
    os.makedirs("static/charts", exist_ok=True)
    chart_file = generate_chart(USER_FOLDER)
    print(f"Graphique sauvegardé ici : {chart_file}")
