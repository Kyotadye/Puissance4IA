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
        self.first = True

    def addChild(self, grille, joueur, last_action):
        child = Node(grille, joueur, self, last_action)
        self.children.append(child)

    def is_terminal_state(self):
        if self.grille.nb_coups >= 42:
            return True
        if len(self.grille.indices_cases_accessibles()) <= 0:
            return True
        elif self.grille.verif_victoire():
            return True
        return False

    def reward_fct(self, joueur):
        if self.grille.verif_victoire():
            if joueur == self.grille.joueur_actuel:
                # print("VICTOIRE")
                return 50
            else:
                # print("DEFAITE")
                return 1
        else:
            # print("NUL")
            return 0


class mcts:
    def utcsearch(self, grille, joueur):
        root = Node(grille, joueur)
        for i in range(10000):
            node = self.treePolicy(root)
            self.defaultPolicy(node)
            #self.backup(node, reward)
        for i in range(len(root.children)):
            print("REWARD GOSSE : ", i, ":", root.children[i].reward)
            print("VISITS GOSSE : ", i, ":", root.children[i].visits)
            print("ACTION GOSSE : ", i, ":", root.children[i].last_action)
        print("GOSSES : ", len(root.children))
        print(root.reward)
        print(root.visits)
        time.sleep(1)
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
        '''print("COUPS POSSIBLES : ", coups_possibles)
        print("COUPS RESTANTS : ", coups_restants)
        print("GOSSES : ",len(node.children))
        time.sleep(1)'''
        if not coups_possibles:
            node.isFullyExpanded = True
            return node
        if coups_restants and not node.isFullyExpanded:
            coup = random.choice(coups_restants)
            grille_copie = cp.deepcopy(node.grille)
            grille_copie.joueur_actuel = node.joueur
            grille_copie.placer_jeton(coup)
            '''print("GRILLE COPIE")
            grille_copie.afficher_grille()
            time.sleep(1)'''
            node.addChild(grille_copie, 3 - node.joueur, coup)
            return node.children[-1]
        return node

    def bestChild(self, node):
        bestscore = -np.inf
        bestchildren = []
        for child in node.children:
            exploit = child.reward / child.visits
            explore = 1.5 * np.sqrt((2.0 * np.log(node.visits)) / child.visits)
            # print("EXPLOIT",exploit)
            # print("EXPLORE",explore)
            score = exploit + explore
            # print("SCORE",score)
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
            self.backup(node, node.reward_fct(self.joueur))
        #return node.reward_fct(self.joueur)

    def backup(self, node, reward):
        while node is not None:
            node.visits += 1
            # print(node.joueur)
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
