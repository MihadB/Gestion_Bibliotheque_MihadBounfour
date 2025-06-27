import json
import os
import csv
from datetime import datetime
from exceptions import (
    LivreIndisponibleError,
    QuotaEmpruntDepasseError,
    MembreInexistantError,
    LivreInexistantError
)


class Livre:
    def __init__(self,ISBN, titre, auteur, annee, genre):
        self.ISBN = ISBN
        self.titre = titre
        self.auteur = auteur
        self.annee = annee
        self.genre = genre
        self.statut = "disponible"  # Par défaut disponible

    def __str__(self):
        return f"{self.titre} par {self.auteur} ({self.annee}) - {self.genre} [{'OK' if self.statut == 'disponible' else 'NON'}]"

    def emprunter(self):
        if self.statut == "disponible":
            self.statut = "emprunté"
            return True
        return False

    def retourner(self):
        self.statut = "disponible"


#CLASSE MEMBRE
class Membre:
    def __init__(self, ID, nom):
        self.ID = ID
        self.nom = nom
        self.livres_empruntes = []

    def __str__(self):
        return f"{self.nom} (ID: {self.ID}) - {len(self.livres_empruntes)} livre(s) emprunté(s)"

    def emprunter_livre(self, livre: Livre):
        if livre.emprunter():
            self.livres_empruntes.append(livre.ISBN)
            return True
        return False

    def retourner_livre(self, livre:Livre):
        if livre.isbn in self.livres_empruntes:
           livre.retourner()
           self.livres_empruntes.remove(livre.isbn)
           return True
        return False

       
#CLASSE BIBLIOTHEQUE
class Bibliotheque:
    def __init__(self):
        self.livres = {}  # Dictionnaire {ISBN: Livre}
        self.membres = {}  # Dictionnaire {ID: Membre}
        self.historique = []

    # Méthodes pour les livres
    def ajouter_livre(self, livre: Livre):
        if livre.ISBN in self.livres:
            return False
        self.livres[livre.ISBN] = livre
        return True

    def supprimer_livre(self, ISBN: str):
        if ISBN in self.livres:
            del self.livres[ISBN]
            return True
        return False

    # Méthodes pour les membres
    def enregistrer_membre(self, membre: Membre):
        if membre.ID in self.membres:
            return False
        self.membres[membre.ID] = membre
        return True

    # Gestion des emprunts
    def emprunter_livre(self, ISBN,ID):
        if ISBN not in self.livres or ID not in self.membres:
            return False
        
        livre = self.livres[ISBN]
        membre = self.membres[ID]
        
        if membre.emprunter_livre(livre):
            self.historique.append({
                'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'isbn': ISBN,
                'id_membre': ID,
                'action': 'emprunt'
            })
            return True
        return False

    def retourner_livre(self,ISBN, ID):
        if ISBN not in self.livres :
            raise  LivreInexistantError()
        if ID not in self.membres:
            raise  MembreInexistantError()
        
        if ISBN not in self.membres[ID].livres_empruntes:
            raise ValueError("Ce membre n'a pas emprunté ce livre")
        
        self.livres[ISBN].statut = "disponible"
        self.membres[ID].livres_empruntes.remove(ISBN)

        self.historique.append({
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'isbn': ISBN,
            'id_membre': ID,
            'action': 'retour'
        })
        return True 

    # Persistance des données
    def sauvegarder_livre (self):
        try:
            # 1. Sauvegarde des livres (format TXT)
            with open('data/livres.txt', 'w', encoding='utf-8') as f:
                for ISBN, livre in self.livres.items():
                    ligne = f"{ISBN};{livre.titre};{livre.auteur};{livre.annee};{livre.genre};{livre.statut}\n"
                    f.write(ligne)

           
            return True
        
        except Exception as e:
            print(f"ERREUR lors de la sauvegarde: {str(e)}")
            return False   
        

    def sauvegarder_donnees(self):

        try:
            # 1. Sauvegarde des livres (format TXT)
            with open('data/livres.txt', 'a', encoding='utf-8') as f:
                for ISBN, livre in self.livres.items():
                    ligne = f"{ISBN};{livre.titre};{livre.auteur};{livre.annee};{livre.genre};{livre.statut}\n"
                    f.write(ligne)

            # 2. Sauvegarde des membres (format TXT)
            with open('data/membres.txt', 'a', encoding='utf-8') as f:
                for ID, membre in self.membres.items():
                    livres_empruntes = ','.join(membre.livres_empruntes)
                    ligne = f"{ID};{membre.nom};{livres_empruntes}\n"
                    f.write(ligne)
            
            # 3. Sauvegarde de l'historique (format CSV)
            with open('data/historique.csv', 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f, delimiter=';')
                writer.writerow(['Date', 'ISBN', 'ID', 'Action'])

                for transaction in self.historique:
                    writer.writerow([
                        transaction['date'],
                        transaction['isbn'],
                        transaction['id_membre'],
                        transaction['action']
                    ])
                    
            return True
        
        except Exception as e:
            print(f"ERREUR lors de la sauvegarde: {str(e)}")
            return False
        

    def charger_donnees(self):

        # 1. Chargement des livres
        try:
            self.livres = {}
            if os.path.exists('data/livres.txt'):
                with open('data/livres.txt', 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            ISBN, titre, auteur, annee, genre, statut = line.split(';')
                            livre = Livre(ISBN, titre, auteur, annee, genre)
                            livre.statut = statut
                            self.livres[ISBN] = livre

        #2. Chargement des membres
            self.membres = {}
            if os.path.exists('data/membres.txt'):
                with open('data/membres.txt', 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            parts = line.split(';')
                            membre = Membre(parts[0], parts[1])
                            if len(parts) > 2 and parts[2]:
                                membre.livres_empruntes = parts[2].split(',')
                            self.membres[membre.id] = membre
        
        # 3. Chargement de l'historique
            self.historique = []
            if os.path.exists('data/historique.csv'):
                with open('data/historique.csv', 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f, delimiter=';')
                    for row in reader:
                        self.historique.append({
                            'date': row['Date'],
                            'ID': row['ID'],
                            'action': row['Action']
                        })
            return True
        
        except Exception as e:
            print(f"ERREUR lors du chargement: {str(e)}")
            return False


            


        



        
            


        
        

    
                                  



            
             



    