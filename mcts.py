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
        self.visits = 0
        self.children = []
        self.isFullyExpanded = False

    def addChild(self, grille, joueur, last_action):
        child = Node(grille, joueur, self, last_action)
        self.children.append(child)

    def update(self, reward):
        self.reward += reward
        self.visits += 1
        self.isFullyExpanded = True

    def is_terminal_state(self):
        if self.grille.verif_victoire():
            if self.joueur == self.grille.joueur_actuel:
                self.update(1)
            else:
                self.update(-1)
            return True
        elif len(self.grille.indices_cases_accessibles()) <= 0:
            self.update(0)
            return True
        return False

    def expand(self):
        coups_possibles = self.grille.indices_cases_accessibles()
        for coup in coups_possibles:
            grille_copie = cp.deepcopy(self.grille)
            grille_copie.joueur_actuel = self.joueur
            grille_copie.placer_jeton(coup[1])
            self.addChild(grille_copie, 3 - self.joueur, coup[1])
            self.children[-1].last_action = coup[1]
        self.isFullyExpanded = len(self.children) == len(coups_possibles) or len(self.children) == 0

    def get_next_state(self):
        if not self.isFullyExpanded or len(self.children) == 0:
            self.expand()
        return random.choice(self.children)

    def reward_fct(self):
        if self.grille.verif_victoire():
            if self.joueur == self.grille.joueur_actuel:
                return 1
            else:
                return -1
        else:
            return 0

class mcts:
    def utcsearch(self, grille, joueur):
        root = Node(grille, joueur)
        for i in range(1000):
            node = self.treePolicy(root)
            reward = self.defaultPolicy(node)
            self.backup(node, reward)
        bestchild = self.bestChild(root)
        return bestchild.last_action

    def treePolicy(self, node):
        while not node.is_terminal_state():
            if not node.isFullyExpanded:
                node.expand()
            else:
                node = self.bestChild(node)
        return node

    def bestChild(self, node):
        bestscore = -np.inf
        bestchildren = []
        for child in node.children:
            if child.visits > 0:
                exploit = child.reward / child.visits
                explore = 1.2 * np.sqrt(2.0 * np.log(node.visits) / child.visits)
            else:
                exploit = -np.inf
                explore = -np.inf
            score = exploit + explore
            if score == bestscore:
                bestchildren.append(child)
            if score > bestscore:
                bestchildren = [child]
                bestscore = score
        if len(bestchildren) == 0:
            return node
        res = random.choice(bestchildren)
        return res

    def defaultPolicy(self, node):
        current_state = node
        while not current_state.is_terminal_state():
            current_state = current_state.get_next_state()
        reward = current_state.reward_fct()
        return reward

    def backup(self, node, reward):
        while node is not None:
            node.visits += 1
            node.reward += reward
            node = node.parent
            #node.update(reward)

    def __init__(self, grille):
        self.grille = grille
        self.joueur = 1

    def jouer_puissance4(self):
        while not self.grille.fin_jeu:
            self.grille.afficher_grille()
            # time.sleep(1)
            # Demande à l'utilisateur de choisir la colonne
            if self.grille.joueur_actuel == 2:
                self.joueur = 2
                self.grille.placer_jeton(self.utcsearch(self.grille, 2))
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
            # Changer de joueur
            self.grille.joueur_actuel = 3 - self.grille.joueur_actuel
