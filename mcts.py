import copy as cp
import math
import random

import numpy as np


class mcts:
    def __init__(self, grille, joueur):
        self.grille = grille
        self.joueur = joueur

    def utcsearch(self, grille,joueur):
        state = State(grille, joueur)
        root = Node(state)
        for i in range(1):
            node = self.treePolicy(root)
            reward = self.defaultPolicy(node)
            self.backup(node, reward)
        bestchild = self.bestChild(root)
        return bestchild.state.last_action

    def treePolicy(self, node):
        while not node.state.is_terminal_state():
            if not node.isFullyExpanded:
                return self.expand(node)
            else:
                node = self.bestChild(node)
        return node

    def expand(self, node):
        tried_children = [child.state for child in node.children]
        new_state = node.state.get_next_state()
        while new_state in tried_children:
            new_state = node.state.get_next_state()
        node.addChild(new_state)
        return node.children[-1]

    def bestChild(self, node):
        bestscore = -np.inf
        bestchildren = []
        for child in node.children:
            exploit = child.reward / child.visits
            explore = 1.2*np.sqrt(2.0 * np.log(node.visits) / child.visits)
            score = exploit + explore
            print("Child:", child.state.last_action)
            print("Exploit:", exploit)
            print("Explore:", explore)
            print("Score:", score)
            if score == bestscore:
                bestchildren.append(child)
            if score > bestscore:
                bestchildren = [child]
                bestscore = score
        return random.choice(bestchildren)

    def defaultPolicy(self, node):
        current_state = node.state
        while not current_state.is_terminal_state():
            current_state = current_state.get_next_state()
        return current_state.reward()

    def backup(self, node, reward):
        while node != None:
            node.visits += 1
            node.reward += reward
            node = node.parent

    def jouer_puissance4(self):
        while not self.grille.fin_jeu:
            # self.grille.afficher_grille()
            # time.sleep(1)
            # Demande à l'utilisateur de choisir la colonne
            if self.grille.joueur_actuel == 1:
                self.grille.placer_jeton(self.utcsearch(self.grille,1))
                self.joueur = 1
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
                self.grille.afficher_grille()
                if (self.grille.joueur_actuel == 2):
                    return 1
                print(f"Joueur {self.grille.joueur_actuel} a gagné !")
                return 0
            elif self.grille.nb_coups == self.grille.taille_grille[0] * self.grille.taille_grille[1]:
                self.grille.afficher_grille()
                print("Match nul !")
                self.grille.fin_jeu = True
                return 0
            self.grille.afficher_grille()
            # Changer de joueur
            self.grille.joueur_actuel = 3 - self.grille.joueur_actuel


class Node:
    def __init__(self, state, parent=None):
        self.state = state
        self.isFullyExpanded = False
        self.parent = parent
        self.reward = 0
        self.visits = 0
        self.children = []

    def addChild(self, state):
        child = Node(state, self)
        self.children.append(child)

    def update(self, reward):
        self.reward += reward
        self.visits += 1
        self.isFullyExpanded = True

    def __repr__(self):
        s = "Node; children: %d; visits: %d; reward: %f" % (len(self.children), self.visits, self.reward)
        return s


class State:
    def __init__(self, grille, joueur):
        self.grille = grille
        self.joueur = joueur
        self.nb_visites = 0
        self.recompense = 0
        self.enfants = []
        self.last_action = 0

    def is_terminal_state(self):
        return self.grille.verif_victoire() or self.grille.nb_coups == self.grille.taille_grille[0] * self.grille.taille_grille[1]

    def expand(self):
        coups_possibles = self.grille.indices_cases_accessibles()
        for coup in coups_possibles:
            grille_copie = cp.deepcopy(self.grille)
            grille_copie.joueur_actuel = self.joueur
            grille_copie.placer_jeton(coup[1])
            enfant = State(grille_copie, 3 - self.joueur)
            self.enfants.append(enfant)
            self.last_action = coup[1]

    def update(self, recompense):
        self.nb_visites += 1
        self.recompense += recompense

    def get_next_state(self):
        if not self.enfants:
            self.expand()
        return random.choice(self.enfants)

    def reward(self):
        if self.grille.verif_victoire():
            if self.joueur == self.grille.joueur_actuel:
                return 1
            else:
                return -1
        else:
            return 0
