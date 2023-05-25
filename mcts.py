import copy as cp
import math
import random

import numpy as np


class mcts:
    def __init__(self, grille, joueur):
        self.grille = grille
        self.joueur = joueur

    def utcsearch(self, node):
        for i in range(100):
            node = self.treePolicy(node)
            reward = self.defaultPolicy(node)
            self.backup(node, reward)

    def treePolicy(self, node):
        while not node.isTerminal():
            if not node.isFullyExpanded():
                return self.expand(node)
            else:
                node = self.bestChild(node)
        return node

    def expand(self, node):
        tried_children = [child.state for child in node.children]
        new_state = node.state.next_state()
        while new_state in tried_children:
            new_state = node.state.next_state()
        node.addChild(new_state)
        return node.children[-1]

    def bestChild(self, node):
        bestscore = -np.inf
        bestchildren = []
        for child in node.children:
            exploit = child.reward / child.visits
            explore = np.sqrt(2.0 * np.log(node.visits) / child.visits)
            score = exploit + explore
            if score == bestscore:
                bestchildren.append(child)
            if score > bestscore:
                bestchildren = [child]
                bestscore = score
        return random.choice(bestchildren)

    def defaultPolicy(self, node):
        current_state = node.state
        while not current_state.isTerminal():
            current_state = current_state.next_state()
        return current_state.reward()

    def backup(self, node, reward):
        while node != None:
            node.visits += 1
            node.reward += reward
            node = node.parent


class Node:
    def __init__(self, state, parent=None):
        self.state = state
        self.isTerminal = state.isTerminal()
        self.isFullyExpanded = self.isTerminal
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

    def selectionner_enfant_ucb(self):
        enfant_ucb = max(self.enfants, key=lambda e: e.recompense / e.nb_visites + math.sqrt(
            2 * math.log(self.nb_visites) / e.nb_visites))
        return enfant_ucb

    def expand(self):
        coups_possibles = self.grille.indices_cases_accessibles()

        for coup in coups_possibles:
            grille_copie = cp.deepcopy(self.grille)
            grille_copie.joueur_actuel = self.joueur
            grille_copie.placer_jeton(coup[1])
            enfant = State(grille_copie, 3 - self.joueur)
            self.enfants.append(enfant)

    def update(self, recompense):
        self.nb_visites += 1
        self.recompense += recompense

    def is_terminal(self):
        return self.grille.verif_victoire() or self.grille.nb_coups == self.grille.taille_grille[0] * \
            self.grille.taille_grille[1]

    def next_state(self):
        return random.choice(self.enfants)

    def reward(self):
        if self.grille.verif_victoire():
            if self.joueur == self.grille.joueur_actuel:
                return 1
            else:
                return -1
        else:
            return 0

    def __repr__(self):
        s = "State; children: %d; visits: %d; reward: %f" % (len(self.enfants), self.nb_visites, self.recompense)
        return s
