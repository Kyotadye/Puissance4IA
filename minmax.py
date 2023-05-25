import copy as cp
import random

import numpy as np


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
            return None, evalu
        max_eval = -np.inf
        max_colonne = 0
        if self.joueur == 2:
            actuel = False
        if actuel:
            joueur_actuel = self.joueur
            joueur_autre = 3 - self.joueur
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
            joueur_autre = self.joueur
            joueur_actuel = 3 - self.joueur
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
            if self.grille.joueur_actuel == 2:
                self.grille.placer_jeton(self.minmaxfunc())
                self.joueur = 2
            else:
                pose = False
                while not pose:
                    colonne = random.randint(0, 6)
                    if self.grille.grille[0][colonne] == 0:
                        self.grille.placer_jeton(colonne)
                        pose = True
            self.grille.nb_coups += 1
            if self.grille.verif_victoire():
                self.grille.fin_jeu = True
                if self.grille.joueur_actuel == 2:
                    return 1
                self.grille.afficher_grille()
                print(f"Joueur {self.grille.joueur_actuel} a gagné !")
                return 0
            elif self.grille.nb_coups == self.grille.taille_grille[0] * self.grille.taille_grille[1]:
                self.grille.afficher_grille()
                print("Match nul !")
                self.grille.fin_jeu = True
                return 0

            # Changer de joueur
            self.grille.joueur_actuel = 3 - self.grille.joueur_actuel
