import numpy as np


class puissance4:
    def __init__(self):
        self.taille_grille = (6, 7)
        self.grille = np.zeros(self.taille_grille, dtype=int)
        self.joueur_actuel = 1
        self.nb_coups = 0
        self.fin_jeu = False
        self.last_move = [0, 0]

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
        for i in range(self.taille_grille[0] - 1, -1, -1):
            if self.grille[i][colonne] == 0:
                self.grille[i][colonne] = self.joueur_actuel
                self.last_move = [i, colonne]
                break

    def verif_victoire(self):
        joueur = self.joueur_actuel
        last_row, last_col = self.last_move

        # Check horizontal line
        count = 0
        start_col = max(0, last_col - 3)
        end_col = min(last_col + 4, self.taille_grille[1])
        for col in range(start_col, end_col):
            if self.grille[last_row][col] == joueur:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0

        # Check vertical line
        count = 0
        start_row = max(0, last_row - 3)
        end_row = min(last_row + 4, self.taille_grille[0])
        for row in range(start_row, end_row):
            if self.grille[row][last_col] == joueur:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0

        for i in range(self.taille_grille[0] - 3):
            for j in range(self.taille_grille[1] - 3):
                if np.all(np.diag(self.grille[i:i + 4, j:j + 4]) == joueur):
                    return True

        # Vérification des diagonales descendantes
        for i in range(self.taille_grille[0] - 3):
            for j in range(self.taille_grille[1] - 3):
                if np.all(np.diag(np.fliplr(self.grille[i:i + 4, j:j + 4])) == joueur):
                    return True

        return False

    '''def verif_victoire(self):
        joueur = self.joueur_actuel

        # Vérification des lignes
        for i in range(self.taille_grille[0]):
            for j in range(self.taille_grille[1] - 3):
                if np.all(self.grille[i, j:j + 4] == joueur):
                    return True

        # Vérification des colonnes
        for i in range(self.taille_grille[0] - 3):
            for j in range(self.taille_grille[1]):
                if np.all(self.grille[i:i + 4, j] == joueur):
                    return True

        # Vérification des diagonales ascendantes
        for i in range(self.taille_grille[0] - 3):
            for j in range(self.taille_grille[1] - 3):
                if np.all(np.diag(self.grille[i:i + 4, j:j + 4]) == joueur):
                    return True

        # Vérification des diagonales descendantes
        for i in range(self.taille_grille[0] - 3):
            for j in range(self.taille_grille[1] - 3):
                if np.all(np.diag(np.fliplr(self.grille[i:i + 4, j:j + 4])) == joueur):
                    return True

        return False'''

    def evaluer(self, joueur):
        joueur_autre = 3 - joueur
        eval = 0

        # Évaluation des lignes horizontales
        for i in range(self.taille_grille[0]):
            for j in range(self.taille_grille[1] - 3):
                ligne = self.grille[i, j:j + 4]
                eval += self.evaluer_ligne_joueur(ligne, joueur, False)
                eval += self.evaluer_ligne_joueur(ligne, joueur_autre, True)

        # Évaluation des lignes verticales
        for j in range(self.taille_grille[1]):
            for i in range(self.taille_grille[0] - 3):
                ligne = np.flip(self.grille[i:i + 4, j])
                eval += self.evaluer_ligne_joueur(ligne, joueur, False)
                eval += self.evaluer_ligne_joueur(ligne, joueur_autre, True)

        # Évaluation des diagonales montantes
        for i in range(self.taille_grille[0] - 3):
            for j in range(self.taille_grille[1] - 1, 2, -1):
                diagonale = np.flip([self.grille[i + k][j - k] for k in range(4)])
                eval += self.evaluer_ligne_joueur(diagonale, joueur, False)
                eval += self.evaluer_ligne_joueur(diagonale, joueur_autre, True)

        # Évaluation des diagonales descendantes
        for i in range(self.taille_grille[0] - 3):
            for j in range(self.taille_grille[1] - 1, 2, -1):
                x = self.taille_grille[1] - j - 1
                diagonale = np.flip([self.grille[i + k][x + k] for k in range(4)])
                eval += self.evaluer_ligne_joueur(diagonale, joueur, False)
                eval += self.evaluer_ligne_joueur(diagonale, joueur_autre, True)

        return eval

    def evaluer_ligne_joueur(self, ligne, joueur, autre):
        eval_list = []
        negatif = 1
        if autre:
            negatif = -1
        if np.all(ligne == joueur):
            eval_list.append(1000 * negatif)
        elif np.all(ligne[:-1] == joueur) and ligne[-1] == 0:
            eval_list.append(50 * negatif)
        elif np.all(ligne[:-2] == joueur) and (ligne[-2] == 0 or ligne[-1] == 0):
            eval_list.append(5 * negatif)
        elif ligne[0] == joueur and (ligne[1] == 0 or ligne[0] == 0) and (ligne[2] == 0 or ligne[1] == 0) and (
                ligne[3] == 0 or ligne[2] == 0):
            eval_list.append(1 * negatif)
        if len(eval_list) == 0:
            return 0
        if autre:
            return min(eval_list)
        return max(eval_list)

    def indices_cases_accessibles(self):
        indices_accessibles = []
        taille_grille = self.grille.shape

        for colonne in range(taille_grille[1]):
            for ligne in range(taille_grille[0] - 1, -1, -1):
                if self.grille[ligne][colonne] == 0:
                    indices_accessibles.append(colonne)
        return indices_accessibles
