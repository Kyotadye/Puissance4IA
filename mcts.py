import time
import numpy as np
import random
import copy as cp


class Node:
    def __init__(self, grille, joueur, parent=None, last_action=0):
        self.grille = grille  # La grille de jeu associée à ce nœud
        self.joueur = joueur  # Le joueur associé à ce nœud
        self.parent = parent  # Le nœud parent dans l'arbre de recherche
        self.last_action = last_action  # L'action qui a conduit à ce nœud
        self.reward = 0  # La récompense cumulée jusqu'à présent pour ce nœud
        self.visits = 1  # Le nombre de visites pour ce nœud
        self.children = []  # Les enfants de ce nœud
        self.isFullyExpanded = False  # Indicateur pour vérifier si le nœud est complètement étendu
        self.first = True  # Indicateur pour marquer le premier nœud

    def addChild(self, grille, joueur, last_action):
        child = Node(grille, joueur, self, last_action)
        self.children.append(child)

    def is_terminal_state(self):
        if self.grille.nb_coups >= 42:  # Si tous les coups ont été joués et la grille est pleine
            return True
        if len(self.grille.indices_cases_accessibles()) <= 0:  # Si aucun coup possible dans la grille
            return True
        elif self.grille.verif_victoire():  # Si un joueur a remporté la partie
            return True
        return False

    def reward_fct(self, joueur):
        if self.grille.verif_victoire():
            if joueur == self.grille.joueur_actuel:  # Si le joueur associé à ce nœud a gagné
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

        # Effectue une recherche Monte Carlo Tree Search pour un certain nombre d'itérations
        for i in range(10000):
            node = self.treePolicy(root)
            self.defaultPolicy(node)
            # self.backup(node, reward)

        # Sélectionne le meilleur enfant à partir du nœud racine
        print("Nombre de noeuds : ", self.compter_noeuds(root))
        print("Nombre de niveaux : ", self.compter_niveau(root))
        time.sleep(1)
        bestchild = self.bestChild(root, 0)
        return bestchild.last_action

    def compter_noeuds(self, node):
        if node.children == []:
            return 1
        else:
            return 1 + sum([self.compter_noeuds(child) for child in node.children])

    def compter_niveau(self, node):
        if node.children == []:
            return 1
        else:
            return 1 + max([self.compter_niveau(child) for child in node.children])

    def treePolicy(self, node):
        # Applique la politique de sélection de l'arbre jusqu'à atteindre un nœud terminal
        while not node.is_terminal_state():
            if not node.isFullyExpanded:
                return self.expand(node)
            else:
                node = self.bestChild(node, 1.5)
        return node

    def expand(self, node):
        coups_possibles = node.grille.indices_cases_accessibles()
        coups_restants = [coup for coup in coups_possibles if
                          coup not in [child.last_action for child in node.children]]
        '''print("COUPS POSSIBLES : ", coups_possibles)
        print("COUPS RESTANTS : ", coups_restants)
        print("GOSSES : ",len(node.children))
        time.sleep(1)'''

        # Si aucun coup possible ou tous les coups ont déjà été explorés, marquer le nœud comme complètement étendu
        if not coups_possibles or len(coups_restants) == 0:
            node.isFullyExpanded = True
            return node

        # Si des coups restent à explorer, en choisir un aléatoirement et ajouter un nouvel enfant au nœud actuel
        coup = random.choice(coups_restants)
        grille_copie = cp.deepcopy(node.grille)
        grille_copie.joueur_actuel = node.joueur
        grille_copie.placer_jeton(coup)
        '''print("GRILLE COPIE")
        grille_copie.afficher_grille()
        time.sleep(1)'''
        node.addChild(grille_copie, 3 - node.joueur, coup)
        return node.children[-1]


    def bestChild(self, node, c):
        bestscore = -np.inf
        bestchildren = []

        # Trouve le meilleur score parmi les enfants du nœud donné
        for child in node.children:
            exploit = child.reward / child.visits
            explore = c * np.sqrt((2.0 * np.log(node.visits)) / child.visits)
            # print("EXPLOIT",exploit)
            # print("EXPLORE",explore)
            score = exploit + explore
            # print("SCORE",score)

            # Si le score est égal au meilleur score, ajoute l'enfant à la liste des meilleurs enfants
            if score == bestscore:
                bestchildren.append(child)
            # Si le score est meilleur que le meilleur score précédent, met à jour la liste des meilleurs enfants
            if score > bestscore:
                bestchildren = [child]
                bestscore = score

        # Choisi un enfant aléatoire parmi les meilleurs enfants
        res = random.choice(bestchildren)
        return res

    def defaultPolicy(self, node):
        # Effectue une politique par défaut aléatoire jusqu'à atteindre un nœud terminal
        while not node.is_terminal_state():
            node = random.choice(node.children) if node.children else self.expand(node)
            self.backup(node, node.reward_fct(self.joueur))
        # return node.reward_fct(self.joueur)

    def backup(self, node, reward):
        # Remonte l'arbre et met à jour les récompenses et les visites des nœuds
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
