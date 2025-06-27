BOUNFOUR MIHAD 
1. instalation et configuration
Prérequis:
Python 3.x installé
Bibliothèques requises :
   pip install matplotlib 
2.Lancement de l'application
python main.py

3. Fonctionnalités et Mode d'Emploi:
   📚 Gestion des Livres
Ajouter un livre	     Menu →  Gestion des livres →  Ajouter
Supprimer un livre	   Menu →  Gestion des livres →  Supprimer (saisir l'ISBN)
Rechercher un livre	   Menu →  Gestion des livres →  Rechercher (par titre/auteur/genre)
   👥 Gestion des Membres:

Enregistrer un membre	  Menu →  Gestion des membres → Enregistrer
Consulter les emprunts	Menu →  Emprunts →  Lister les emprunts

   🔄 Emprunts & Retours :

Emprunter un livre	Menu →  Emprunts →  Emprunter (saisir ISBN + ID membre)
Retourner un livre	Menu →  Emprunts →  Retourner (saisir ISBN)
    💾 Sauvegarde des Données:
Les données sont automatiquement sauvegardées dans :

data/livres.txt (liste des livres)
data/membres.txt (liste des membres)
data/historique.csv (historique des transactions)

