import matplotlib.pyplot as plt
from collections import Counter

class Visualisation:
    
    def stats_genres(livres):
        """Génère un camembert des genres"""
        genres = [livre.genre for livre in livres.values()]
        counter = Counter(genres)
        
        plt.figure(figsize=(8, 6))
        plt.pie(counter.values(), labels=counter.keys(), autopct='%1.1f%%')
        plt.title("Répartition des livres par genre")
        return plt

    
    def stats_auteurs(livres):
        """Génère un histogramme des auteurs"""
        auteurs = [livre.auteur for livre in livres.values()]
        counter = Counter(auteurs).most_common(10)  # Top 10
        
        plt.figure(figsize=(10, 5))
        plt.bar([a[0] for a in counter], [a[1] for a in counter])
        plt.xticks(rotation=45, ha='right')
        plt.title("Top 10 des auteurs")
        plt.tight_layout()
        return plt