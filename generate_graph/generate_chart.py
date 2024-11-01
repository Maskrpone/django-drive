import matplotlib.pyplot as plt

def generate_storage_chart(data):
    """
    Génère un graphique à secteurs représentant la répartition de l'espace par format et l'affiche.

    :param data: Un dictionnaire contenant le format des fichiers et leur taille 
                 (par exemple : {"Images": 500, "Documents": 300, "Vidéos": 200, "Autres": 100})
    """
    labels = list(data.keys())
    sizes = list(data.values())

    # Création du graphique
    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')  # Assure un cercle
    plt.title("Répartition de l'espace par format")
    
    # Enregistrer l'image en local
    plt.savefig("storage_chart.png")
    print("Graphique sauvegardé sous 'storage_chart.png'")

    # Afficher l'image directement
    plt.show()

# Exemple de données pour le graphique
data = {
    "Images": 500,
    "Documents": 300,
    "Vidéos": 200,
    "Autres": 100,
}

generate_storage_chart(data)
