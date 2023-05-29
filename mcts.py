import time

import numpy as np
import random
import copy as cp


class Node:
    def __init__(self, grille, joueur, parent=None, last_action=0):
        self.grille = grille
        self.joueur = joueur
        self.parent = parent
        self.last_action = last_action
        self.reward = 0
        self.visits = 1
        self.children = []
        self.isFullyExpanded = False

    def addChild(self, grille, joueur, last_action):
        child = Node(grille, joueur, self, last_action)
        self.children.append(child)

    def is_terminal_state(self):
        if self.grille.verif_victoire():
            return True
        elif len(self.grille.indices_cases_accessibles()) <= 0:
            return True
        return False

    def reward_fct(self, joueur):
        if self.grille.verif_victoire():
            if joueur == self.grille.joueur_actuel:
                self.reward += 1
            else:
                self.reward += -2
        else:
            self.reward += 0.5
        return self.reward


class mcts:
    def utcsearch(self, grille, joueur):
        root = Node(grille, joueur)
        for i in range(10000):
            node = self.treePolicy(root)
            reward = self.defaultPolicy(node)
            self.backup(node, reward)
        bestchild = self.bestChild(root)
        return bestchild.last_action

    def treePolicy(self, node):
        while not node.is_terminal_state():
            if not node.isFullyExpanded:
                return self.expand(node)
            else:
                node = self.bestChild(node)
        return node

    def expand(self, node):
        coups_possibles = node.grille.indices_cases_accessibles()
        coups_restants = [coup for coup in coups_possibles if
                          coup not in [child.last_action for child in node.children]]
        if not coups_possibles:
            node.isFullyExpanded = True
            return node
        if len(node.children) == len(coups_possibles):
            node.isFullyExpanded = True
        if coups_restants:
            coup = random.choice(coups_restants)
            grille_copie = cp.deepcopy(node.grille)
            grille_copie.joueur_actuel = node.joueur
            grille_copie.placer_jeton(coup)
            '''print("GRILLE COPIE")
            grille_copie.afficher_grille()
            time.sleep(2)'''
            node.addChild(grille_copie, 3 - node.joueur, coup)
            return node.children[-1]
        return node

    def bestChild(self, node):
        bestscore = -np.inf
        bestchildren = []
        for child in node.children:
            exploit = child.reward / child.visits
            explore = 1.2 * np.sqrt(2.0 * np.log(node.visits) / child.visits)
            score = exploit + explore
            if score == bestscore:
                bestchildren.append(child)
            if score > bestscore:
                bestchildren = [child]
                bestscore = score
        res = random.choice(bestchildren)
        return res

    def defaultPolicy(self, node):
        while not node.is_terminal_state():
            node = random.choice(node.children) if node.children else self.expand(node)
        return node.reward_fct(self.joueur)

    def backup(self, node, reward):
        while node is not None:
            node.visits += 1
            if node.joueur == self.joueur:
                reward = -reward
            else:
                reward = reward
            node.reward += reward
            '''print("VISITS : ", node.visits)
            print("REWARD : ", node.reward)'''
            node = node.parent
        '''if node is None:
            print("NODE IS NONE")
            time.sleep(3)'''

    def __init__(self, grille):
        self.grille = grille
        self.joueur = 1

    def jouer(self, joueur):
        self.joueur = joueur
        self.grille.placer_jeton(self.utcsearch(self.grille, joueur))
