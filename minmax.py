import copy as cp
import random

import numpy as np


class minmax:
    def __init__(self, grille, profondeur,evalval=2):
        self.grille = grille
        self.profondeur = profondeur
        self.joueur = grille.joueur_actuel
        self.evalval = evalval

    def minmaxfunc(self):
        action, eval = self.minmax_rec(self.grille, self.profondeur, True)
        return action

    def minmax_rec(self, grille, profondeur, actuel):
        if profondeur == 0 or grille.verif_victoire():
            evalu = grille.evaluer(self.joueur,self.evalval)
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

    def jouer(self, joueur):
        self.grille.placer_jeton(self.minmaxfunc())
        self.joueur = joueur

