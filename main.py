import numpy as np

class Puissance4:
    def __init__(self):
        self.taille_grille = (6, 7)
        self.grille = np.zeros(self.taille_grille, dtype=int)
        self.joueur_actuel = 1
        self.nb_coups = 0
        self.fin_jeu = False

    def afficher_grille(self):
        for row in self.grille:
            for cell in row:
                if cell == 0:
                    print(".", end=" ")
                elif cell == 1:
                    print("X", end=" ")
                else:
                    print("O", end=" ")
            print()
        print()

    def placer_jeton(self, colonne):
        for i in range(self.taille_grille[0]-1, -1, -1):
            if self.grille[i][colonne] == 0:
                self.grille[i][colonne] = self.joueur_actuel
                break

    def verif_victoire(self):
        joueur = self.joueur_actuel

        # Vérification des lignes
        for i in range(self.taille_grille[0]):
            for j in range(self.taille_grille[1]-3):
                if np.all(self.grille[i, j:j+4] == joueur):
                    return True

        # Vérification des colonnes
        for i in range(self.taille_grille[0]-3):
            for j in range(self.taille_grille[1]):
                if np.all(self.grille[i:i+4, j] == joueur):
                    return True

        # Vérification des diagonales ascendantes
        for i in range(self.taille_grille[0]-3):
            for j in range(self.taille_grille[1]-3):
                if np.all(np.diag(self.grille[i:i+4, j:j+4]) == joueur):
                    return True

        # Vérification des diagonales descendantes
        for i in range(self.taille_grille[0]-3):
            for j in range(self.taille_grille[1]-3):
                if np.all(np.diag(np.fliplr(self.grille[i:i+4, j:j+4])) == joueur):
                    return True

        return False

    def jouer_puissance4(self):
        while not self.fin_jeu:
            self.afficher_grille()

            # Demande à l'utilisateur de choisir la colonne
            colonne = int(input(f"Joueur {self.joueur_actuel}, choisissez la colonne (0-6) : "))

            self.placer_jeton(colonne)
            self.nb_coups += 1

            if self.verif_victoire():
                self.afficher_grille()
                print(f"Joueur {self.joueur_actuel} a gagné !")
                self.fin_jeu = True
            elif self.nb_coups == self.taille_grille[0] * self.taille_grille[1]:
                self.afficher_grille()
                print("Match nul !")
                self.fin_jeu = True

            # Changer de joueur
            self.joueur_actuel = 3 - self.joueur_actuel

# Lancer le jeu
jeu = Puissance4()
jeu.jouer_puissance4()
