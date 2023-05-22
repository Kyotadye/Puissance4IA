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
        for i in range(self.taille_grille[0] - 1, -1, -1):
            if self.grille[i][colonne] == 0:
                self.grille[i][colonne] = self.joueur_actuel
                break

    def verif_victoire(self):
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

        return False

    def jouer_puissance4(self):
        while not self.fin_jeu:
            self.afficher_grille()

            # Demande à l'utilisateur de choisir la colonne
            colonne = int(input(f"Joueur {self.joueur_actuel}, choisissez la colonne (0-6) : "))

            self.placer_jeton(colonne)
            self.nb_coups += 1
            print(self.evaluer())
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

    '''def evaluate_diag(self, player):
        nb_tokens = 0
        nb_empty = 0
        score = 0
        for i in range(4):
            if (self.grille[i][i] == player):
                nb_tokens += 1
            elif (self.grille[i][i] == 0):
                nb_empty += 1
        if (nb_tokens == 4):
            score += 1000
        elif (nb_tokens == 3 and nb_empty == 1):
            score += 50
        elif (nb_tokens == 2 and nb_empty == 2):
            score += 5
        elif (nb_tokens == 1 and nb_empty == 3):
            score += 1
        nb_tokens = 0
        nb_empty = 0
        for i in range(4):
            if (self.grille[i][3 - i] == player):
                nb_tokens += 1
            elif (self.grille[i][3 - i] == 0):
                nb_empty += 1
        if (nb_tokens == 4):
            score += 1000
        elif (nb_tokens == 3 and nb_empty == 1):
            score += 50
        elif (nb_tokens == 2 and nb_empty == 2):
            score += 5
        elif (nb_tokens == 1 and nb_empty == 3):
            score += 1
        return score
   def evaluate_four(self, cells, joueur):
        lst_eval = [1, 5, 50, 1000]
        if (not 3 - joueur in cells) and (joueur in cells):
            return lst_eval[cells.count(joueur) - 1]
        else:
            return 0

    def calculate_eval(self, joueur):
        eval_score = 0
        bz = 0
        for row in range(6):
            for col in range(7):
                if col < 4:
                    bz += self.evaluate_four(
                        [self.grille[row][col],
                         self.grille[row][col + 1],
                         self.grille[row][col + 2],
                         self.grille[row][col + 3]], joueur)
                if row < 3:
                    bz += self.evaluate_four(
                        [self.grille[row][col],
                         self.grille[row + 1][col],
                         self.grille[row + 2][col],
                         self.grille[row + 3][col]], joueur)

                    if col < 4:
                        eval_score += self.evaluate_four(
                            [self.grille[row][col],
                             self.grille[row + 1][col + 1],
                             self.grille[row + 2][col + 2],
                             self.grille[row + 3][col + 3]], joueur)
                    if col > 2:
                        eval_score += self.evaluate_four(
                            [self.grille[row][col],
                             self.grille[row + 1][col - 1],
                             self.grille[row + 2][col - 2],
                             self.grille[row + 3][col - 3]], joueur)
        return eval_score

    def evaluer(self):
        return self.calculate_eval(self.joueur_actuel) - self.calculate_eval(3 - self.joueur_actuel)'''

    def evaluer(self):
        joueur = self.joueur_actuel
        joueur_autre = 3 - self.joueur_actuel
        eval = 0

        # Évaluation des lignes horizontales
        for i in range(self.taille_grille[0]):
            for j in range(self.taille_grille[1] - 3):
                ligne = self.grille[i, j:j + 4]
                eval += self.evaluer_ligne_joueur(ligne, joueur)
                eval += self.evaluer_ligne_autre(ligne, joueur_autre)

        # Évaluation des lignes verticales
        for j in range(self.taille_grille[1]):
            for i in range(self.taille_grille[0] - 3):
                ligne = np.flip(self.grille[i:i + 4, j])
                eval+= self.evaluer_ligne_joueur(ligne, joueur)
                eval+= self.evaluer_ligne_autre(ligne, joueur_autre)

        # Évaluation des diagonales montantes
        for i in range(self.taille_grille[0] - 3):
            for j in range(self.taille_grille[1] - 1, 2, -1):
                diagonale = np.flip([self.grille[i + k][j - k] for k in range(4)])
                eval += self.evaluer_ligne_joueur(diagonale, joueur)
                eval += self.evaluer_ligne_autre(diagonale, joueur_autre)

        # Évaluation des diagonales descendantes
        for i in range(self.taille_grille[0] - 3):
            for j in range(self.taille_grille[1] - 1,2, -1):
                x = self.taille_grille[1]-j-1
                diagonale = np.flip([self.grille[i + k][x + k] for k in range(4)])
                eval += self.evaluer_ligne_joueur(diagonale, joueur)
                eval += self.evaluer_ligne_autre(diagonale, joueur_autre)

        return eval

    def evaluer_ligne_joueur(self, ligne, joueur):
        eval_list = []
        if np.all(ligne == joueur):
            eval_list.append(1000)
        elif np.all(ligne[:-1] == joueur) and ligne[-1] == 0:
            eval_list.append(50)
        elif np.all(ligne[:-2] == joueur) and (ligne[-2] == 0 or ligne[-1] == 0):
            eval_list.append(5)
        elif ligne[0] == joueur and (ligne[1] == 0 or ligne[0] == 0) and (ligne[2] == 0 or ligne[1] == 0) and (
                ligne[3] == 0 or ligne[2] == 0):
            eval_list.append(1)
        if len(eval_list) == 0:
            return 0
        return max(eval_list)

    def evaluer_ligne_autre(self, ligne, joueur_autre):
        eval_list = []
        if np.all(ligne == joueur_autre):
            eval_list.append(-1000)
        elif np.all(ligne[:-1] == joueur_autre) and ligne[-1] == 0:
            eval_list.append(-50)
        elif np.all(ligne[:-2] == joueur_autre) and (ligne[-2] == 0 or ligne[-1] == 0):
            eval_list.append(-5)
        elif ligne[0] == joueur_autre and (ligne[1] == 0 or ligne[-1] == 0) and (ligne[2] == 0 or ligne[-2] == 0) and (
                ligne[3] == 0 or ligne[-3] == 0):
            eval_list.append(-1)
        if len(eval_list) == 0:
            return 0
        return min(eval_list)


    # Lancer le jeu


jeu = Puissance4()
jeu.jouer_puissance4()
