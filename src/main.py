
from bibliotheque import Bibliotheque, Livre,Membre
from data.exceptions import (
    LivreIndisponibleError,
    QuotaEmpruntDepasseError,
    MembreInexistantError,
    LivreInexistantError
)
from visualisation import Visualisation

import os
import sys


class InterfaceCLI:
    def __init__(self):
        self.biblio = Bibliotheque()
        if not self._charger_donnees():
            print("\n⚠ Aucune donnée existante. Nouvelle bibliothèque créée.")

    def _charger_donnees(self):
        """Charge les données en silence (retourne False si échec)"""
        try:
            return self.biblio.charger_donnees()
        except Exception:
            return False

    def _afficher_menu(self):
        print("\n" + "═" * 40)
        print("GESTION BIBLIOTHEQUE".center(40))
        print("═" * 40)
        print("1. Ajouter un livre")
        print("2. Inscrire un membre")
        print("3. Emprunter un livre")
        print("4. Rendre un livre")
        print("5. Lister tous les livres")
        print("6. Afficher les statistiques")
        print("7. Sauvegarder et quitter")
        print("═" * 40)

    def _demander_entree(self, prompt, validation_fn=None):
        """Générique pour les saisies utilisateur"""
        while True:
            try:
                valeur = input(prompt).strip()
                if validation_fn:
                    validation_fn(valeur)
                return valeur
            except ValueError as e:
                print("❌ Erreur: {e}")

    def executer(self):
        while True:
            self._afficher_menu()
            choix = self._demander_entree("Votre choix (1-7): ", lambda x: 1 <= int(x) <= 7 or ValueError("Choix invalide"))

            try:
                if choix == "1":
                    self._ajouter_livre()
                elif choix == "2":
                    self._inscrire_membre()
                elif choix == "3":
                    self._emprunter_livre()
                elif choix == "4":
                    self._retourner_livre()
                elif choix == "5":
                    self._lister_livres()
                elif choix == "6":
                    self._afficher_statistiques()
                elif choix == "7":
                    self._quitter()
            except Exception as e:
                print(f"\n Erreur inattendue: {str(e)}")

    # Méthodes métier 
    def _ajouter_livre(self):
        print("\n--- Ajout d'un livre ---")
        try:

            ISBN = input("ISBN (13 chiffres): ").strip()
            titre = input("Titre: ").strip()
            auteur = input("Auteur: ").strip()
            annee = input("Année: ").strip()
            genre = input("Genre: ").strip()
            staut = input("statut:").strip()

            nouveau_livre = Livre(ISBN, titre, auteur, annee,genre)
               
            if self.biblio.ajouter_livre(nouveau_livre) and self.biblio.sauvegarder_livre():
                print("livre ajouté avec succès!")
                
            else: 
                print("Erreur lors de l'ajout")
        
        except Exception as e:
            print(f" Erreur: {str(e)}")

    def _rendre_livre(self):

        print("Retour d'un livre:")

        try:
            ISBN=input("ISBN du livre à retourner :").strip()
            ID = input("ID du membre: ").strip()

            if self.biblio.retourner_livre(ISBN, ID):
                print("\n Livre retourné avec succès!")
                self.biblio.sauvegarder_donnees() 
            
            else:
                print(f"\n Erreur lors du retour")
        except Exception as e:
            print(f"\nErreur: {str(e)}")      

    def _emprunter_livre(self):

        print("\n--- Emprunt d'un livre ---")
        try:
            ISBN = self._demander_entree("ISBN du livre: ")
            ID = self._demander_entree("ID membre: ")
            
            if self.biblio.emprunter_livre(ISBN, ID):
                print("Emprunt enregistré !")
        except LivreInexistantError:
            print(" Ce livre n'existe pas")
        except MembreInexistantError:
            print(" Membre non enregistré")
        except LivreIndisponibleError:
            print(" Livre déjà emprunté")
        except QuotaEmpruntDepasseError:
            print(" Quota de 5 livres atteint")

    def _quitter(self):
        self.biblio.sauvegarder_donnees()
        print("\n Données sauvegardées.")
        sys.exit(0)

    # Validation 
    def _valider_isbn(self, ISBN):
        if not ISBN.isdigit() or len(ISBN) != 13:
            raise ValueError("ISBN doit contenir 13 chiffres")
        
    
    def _lister_livres(self):
        print("\n=== Liste des livres ===")

        print(f"\n{'ISBN':<15} {'Titre':<25} {'Auteur':<20} {'Statut':<10}")
        
        try:
            with open('data/livres.txt', 'r', encoding='utf-8') as f:
                lignes = f.readlines()

                if not lignes:
                    print("Aucun livre trouvé dans le fichier.")
                    return

                print("Liste des livres :")
                print("ISBN\t\tTitre\t\tAuteur\t\tAnnée\tGenre\tStatut")
                print("-" * 80)

                for ligne in lignes:
                    parts = ligne.strip().split(';')
                    if len(parts) == 6:
                        ISBN, titre, auteur, annee, genre, statut = parts
                        print(f"{ISBN}\t{titre}\t{auteur}\t{annee}\t{genre}\t{statut}")
                    else:
                        print(f"Ligne ignorée (format invalide) : {ligne.strip()}")
        except FileNotFoundError:
            print("Le fichier 'data/livres.txt' est introuvable.")
        except Exception as e:
            print(f"Erreur lors de la lecture du fichier : {e}")


    def _inscrire_membre(self):

        print(" --- INSCRIPTION MEMBRE ---")

        try:
           
           ID = input("ID du membre : ").strip()
           nom = input("Nom complet : ").strip()

           if not ID or not nom:
               raise ValueError("Tous les champs sont obligatoires")
           
           nouveau_membre = Membre(ID,nom)

           if self.biblio.enregistrer_membre(nouveau_membre):
               print("\nMembre inscrit avec succès ")

               self.biblio.sauvegarder_donnees()

           else:
               print("\nErreur : ID déjà utilisé")
        
        except ValueError as e:
             print("\nErreur inattendue : {e}")


    def _afficher_statistiques(self):
        print("\n=== Statistiques ===")

        try:
            print(f"- Livres: {len(self.biblio.livres)}")
            print(f"- Membres: {len(self.biblio.membres)}")
            print(f"- Emprunts en cours: {sum(1 for l in self.biblio.livres.values() if l.statut == 'emprunté')}")
        

        #Graphique des genres
            plt_genres = Visualisation.stats_genres(self.biblio.livres)
            plt_genres.show()

        #Graphique des auteurs
            plt_auteurs = Visualisation.stats_auteurs(self.biblio.livres)
            plt_auteurs.show()

        except ImportError:
            print("\n Les graphiques ne sont pas disponibles (matplotlib requis)")

    
    def _sauvegarder_et_quitter(self):
        if self.biblio.sauvegarder_donnees():
            print("\nDonnées sauvegardées avec succès!")

        else:
            print("\n Erreur lors de la sauvegarde!")
        
        print("\nMerci d'avoir utilisé notre système. Au revoir!")
        exit()

    def executer(self):
        while True:
            self._afficher_menu()
            choix = input("Votre choix (1-7): ").strip()
        
            if choix == "1":
                self._ajouter_livre()
            
            elif choix == "2":
                    self._inscrire_membre()
            elif choix == "3":
                    self._emprunter_livre()
            elif choix == "4":
                    self._rendre_livre()
            elif choix == "5":
                    self._lister_livres()
            elif choix == "6":
                    self._afficher_statistiques()
            elif choix == "7":
                    self._sauvegarder_et_quitter()
    
if __name__ == "__main__":
    if not os.path.exists('data'):
        os.makedirs('data')
    
    try:
        interface = InterfaceCLI()
        interface.executer()
    except KeyboardInterrupt:
        print("\n🛑 Programme interrompu")
        sys.exit(1)
    

       