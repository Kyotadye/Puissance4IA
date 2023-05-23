import math
import time

import numpy as np
import copy as cp
import random


class Puissance4:
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

    def evaluer(self, joueur=1):
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
                    indices_accessibles.append((ligne, colonne))
                    break

        return indices_accessibles


class minmax:
    def __init__(self, grille, profondeur):
        self.grille = grille
        self.profondeur = profondeur
        self.joueur = grille.joueur_actuel

    def minmaxfunc(self):
        action, eval = self.minmax_rec(self.grille, self.profondeur, True)
        return action

    def minmax_rec(self, grille, profondeur, actuel):
        if profondeur == 0 or grille.verif_victoire():
            evalu = grille.evaluer(self.joueur)
            # print("JOUEUR : ",self.joueur)
            # print(evalu)
            return None, evalu

        max_eval = -np.inf
        max_colonne = 0
        if actuel:
            joueur_actuel = grille.joueur_actuel
            joueur_autre = 3 - joueur_actuel
            for colonne in range(grille.taille_grille[1]):
                if grille.grille[0][colonne] == 0:
                    grille_temp = cp.deepcopy(grille)
                    grille_temp.placer_jeton(colonne)

                    grille_temp.joueur_actuel = joueur_autre
                    _, eval_score = self.minmax_rec(grille_temp, profondeur - 1, False)
                    if max_eval < eval_score:
                        max_colonne = colonne
                        max_eval = eval_score
            return max_colonne, max_eval
        else:
            # joueur_actuel = grille.joueur_actuel
            # joueur_autre = 3 - joueur_actuel
            joueur_autre = grille.joueur_actuel
            joueur_actuel = 3 - joueur_autre
            min_eval = np.inf
            min_colonne = 0
            for colonne in range(grille.taille_grille[1]):
                if grille.grille[0][colonne] == 0:
                    grille_temp = cp.deepcopy(grille)
                    grille_temp.joueur_actuel = joueur_actuel
                    grille_temp.placer_jeton(colonne)
                    grille_temp.joueur_actuel = joueur_autre
                    _, eval_score = self.minmax_rec(grille_temp, profondeur - 1, True)
                    if min_eval > eval_score:
                        min_colonne = colonne
                        min_eval = eval_score
            return min_colonne, min_eval

    def jouer_puissance4(self):
        while not self.grille.fin_jeu:
            # self.grille.afficher_grille()
            # time.sleep(1)
            # Demande à l'utilisateur de choisir la colonne
            if self.grille.joueur_actuel == 1:
                self.grille.placer_jeton(self.minmaxfunc())
            else:
                pose = False
                while not pose:
                    colonne = random.randint(0, 6)
                    if self.grille.grille[0][colonne] == 0:
                        self.grille.placer_jeton(colonne)
                        pose = True
            self.grille.nb_coups += 1
            if self.grille.verif_victoire():
                self.grille.afficher_grille()
                print(f"Joueur {self.grille.joueur_actuel} a gagné !")
                self.grille.fin_jeu = True
                return self.grille.joueur_actuel
            elif self.grille.nb_coups == self.grille.taille_grille[0] * self.grille.taille_grille[1]:
                self.grille.afficher_grille()
                print("Match nul !")
                self.grille.fin_jeu = True
                return 0

            # Changer de joueur
            self.grille.joueur_actuel = 3 - self.grille.joueur_actuel
            self.joueur = self.grille.joueur_actuel

class AlphaBeta:
    def __init__(self, grille, profondeur):
        self.grille = grille
        self.profondeur = profondeur
        self.joueur = grille.joueur_actuel

    def alpha_beta(self):
        action, eval = self.alpha_beta_rec(self.grille, self.profondeur, True, -np.inf, np.inf)
        return action

    def alpha_beta_rec(self, grille, profondeur, actuel, alpha, beta):
        if profondeur == 0 or grille.verif_victoire():
            evalu = grille.evaluer(self.joueur)
            return None, evalu

        max_eval = -np.inf
        min_eval = np.inf
        best_action = None

        if actuel:
            joueur_actuel = grille.joueur_actuel
            joueur_autre = 3 - joueur_actuel

            for colonne in range(grille.taille_grille[1]):
                if grille.grille[0][colonne] == 0:
                    grille_temp = cp.deepcopy(grille)
                    grille_temp.placer_jeton(colonne)

                    grille_temp.joueur_actuel = joueur_autre
                    _, eval_score = self.alpha_beta_rec(grille_temp, profondeur - 1, False, alpha, beta)

                    if eval_score > max_eval:
                        max_eval = eval_score
                        best_action = colonne

                    alpha = max(alpha, eval_score)
                    if beta <= alpha:
                        break

            return best_action, max_eval
        else:
            joueur_autre = grille.joueur_actuel
            joueur_actuel = 3 - joueur_autre

            for colonne in range(grille.taille_grille[1]):
                if grille.grille[0][colonne] == 0:
                    grille_temp = cp.deepcopy(grille)
                    grille_temp.joueur_actuel = joueur_actuel
                    grille_temp.placer_jeton(colonne)
                    grille_temp.joueur_actuel = joueur_autre
                    _, eval_score = self.alpha_beta_rec(grille_temp, profondeur - 1, True, alpha, beta)

                    if eval_score < min_eval:
                        min_eval = eval_score
                        best_action = colonne

                    beta = min(beta, eval_score)
                    if beta <= alpha:
                        break

            return best_action, min_eval

    def jouer_puissance4(self):
        while not self.grille.fin_jeu:
            # self.grille.afficher_grille()
            # time.sleep(1)
            # Demande à l'utilisateur de choisir la colonne
            if self.grille.joueur_actuel == 1:
                self.grille.placer_jeton(self.alpha_beta())
            else:
                pose = False
                while not pose:
                    colonne = random.randint(0, 6)
                    if self.grille.grille[0][colonne] == 0:
                        self.grille.placer_jeton(colonne)
                        pose = True
            self.grille.nb_coups += 1
            if self.grille.verif_victoire():
                self.grille.afficher_grille()
                print(f"Joueur {self.grille.joueur_actuel} a gagné !")
                self.grille.fin_jeu = True
                return self.grille.joueur_actuel
            elif self.grille.nb_coups == self.grille.taille_grille[0] * self.grille.taille_grille[1]:
                self.grille.afficher_grille()
                print("Match nul !")
                self.grille.fin_jeu = True
                return 0

            # Changer de joueur
            self.grille.joueur_actuel = 3 - self.grille.joueur_actuel
            self.joueur = self.grille.joueur_actuel


total = 0
max = 50
'''for i in range(max):
    jeu = Puissance4()
    iaaa = minmax(jeu, 3)
    total+=iaaa.jouer_puissance4()
print("Nombre de fois où l'IA gagne contre l'aléatoire :", total"/",max)'''
# jeu.jouer_puissance4()
jeu = Puissance4()
#iaaaaa = AlphaBeta(jeu, 4)
#iaaaaa.jouer_puissance4()
