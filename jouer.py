import numpy as np
import random

from alphabeta import alpha_beta
from mcts import mcts
from minmax import minmax
from puissance4 import puissance4


class jouer:
    def __init__(self):
        self.grille = puissance4()
        self.classchoix = None
        self.choixprof = None
        self.indexchoix = [0, 0]
        self.choixeval = None

    def choix(self):
        self.classchoix = [0, 0]
        choix1 = input("Quel est le nom de la classe du joueur 1 ? (1 minmax, 2 alphabeta, 3 mcts, 4 joueur humain, "
                       "5 random) : ")
        self.indexchoix[0] = int(choix1)
        self.souschoix(int(choix1), 0)
        choix2 = input("Quel est le nom de la classe du joueur 2 ? (1 minmax, 2 alphabeta, 3 mcts, 4 joueur humain, "
                       "5 random) : ")
        self.indexchoix[1] = int(choix2)
        self.souschoix(int(choix2), 1)

    def souschoix(self, choix, index):
        if choix == 1 or choix == 2:
            if self.choixprof == None:
                self.choixprof = [0, 0]
            if self.choixeval == None:
                self.choixeval = [0, 0]
            if self.choixprof[index] == 0:
                self.choixprof[index] = input("Quelle est la profondeur de l'IA ? : ")
            if self.choixeval[index] == 0:
                self.choixeval[index] = input("Quelle est l'évaluation de l'IA ? (1 évaluation position, 2 évaluation "
                                              "combinaison) : ")
            if choix == 1:
                self.classchoix[index] = minmax(self.grille, int(self.choixprof[index]), int(self.choixeval[index]))
            else:
                self.classchoix[index] = alpha_beta(self.grille, int(self.choixprof[index]), int(self.choixeval[index]))
        elif choix == 3:
            self.classchoix[index] = mcts(self.grille)
        elif choix == 4:
            self.classchoix[index] = 0
        elif choix == 5:
            self.classchoix[index] = 1
        else:
            if choix!=0:
                print("Erreur de saisie !")
                self.choix()

    def jeu_random(self):
        pose = False
        while not pose:
            colonne = random.randint(0, 6)
            if self.grille.grille[0][colonne] == 0:
                self.grille.placer_jeton(colonne)
                pose = True

    def jeu_joueur(self):
        colonne = int(input(f"Joueur {self.grille.joueur_actuel}, choisissez la colonne (0-6) : "))
        self.grille.placer_jeton(colonne)

    def jouer_puissance4(self):
        self.reset_jeu()
        if self.classchoix == None:
            self.choix()
        while not self.grille.fin_jeu:
            self.grille.afficher_grille()
            # Demande à l'utilisateur de choisir la colonne
            if self.grille.joueur_actuel == 1:
                if self.classchoix[0] != 0 and self.classchoix[0] != 1:
                    self.classchoix[0].jouer(1)
                elif self.classchoix[0] == 0:
                    self.jeu_joueur()
                elif self.classchoix[0] == 1:
                    self.jeu_random()
            else:
                if self.classchoix[1] != 0 and self.classchoix[1] != 1:
                    self.classchoix[1].jouer(2)
                elif self.classchoix[1] == 0:
                    self.jeu_joueur()
                elif self.classchoix[1] == 1:
                    self.jeu_random()
            self.grille.nb_coups += 1
            if self.grille.verif_victoire():
                self.grille.fin_jeu = True
                self.grille.afficher_grille()
                print(f"Joueur {self.grille.joueur_actuel} a gagné !")
                if self.grille.joueur_actuel == 1:
                    return 1
                return 0
            elif self.grille.nb_coups == self.grille.taille_grille[0] * self.grille.taille_grille[1]:
                self.grille.afficher_grille()
                print("Match nul !")
                self.grille.fin_jeu = True
                return 0
            # Changer de joueur
            self.grille.joueur_actuel = 3 - self.grille.joueur_actuel

    def reset_jeu(self):
        self.grille = puissance4()
        self.souschoix(self.indexchoix[0], 0)
        self.souschoix(self.indexchoix[1], 1)
