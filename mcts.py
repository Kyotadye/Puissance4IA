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

    def update(self, reward):
        self.reward += reward
        self.visits += 1

    def is_terminal_state(self):
        if self.grille.verif_victoire():
            return True
        elif len(self.grille.indices_cases_accessibles()) <= 0:
            return True
        return False

    def get_next_state(self):
        return random.choice(self.children)

    def reward_fct(self, joueur):
        if self.grille.verif_victoire():
            if joueur == self.grille.joueur_actuel:
                self.update(1)
            else:
                self.update(-1)
        else:
            self.update(0)
        return self.reward


class mcts:
    def utcsearch(self, grille, joueur):
        root = Node(grille, joueur)
        for i in range(5000):
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
        for coup in coups_restants:
            grille_copie = cp.deepcopy(node.grille)
            grille_copie.joueur_actuel = node.joueur
            grille_copie.placer_jeton(coup)
            node.addChild(grille_copie, 3 - node.joueur, coup)
            node.children[-1].last_action = coup
            node.children[-1].visits += 1
        if len(node.children) == len(coups_possibles):
            node.isFullyExpanded = True
        return node

    def bestChild(self, node):
        bestscore = -np.inf
        bestchildren = []
        for child in node.children:
            exploit = child.reward / child.visits
            explore = 1.5 * np.sqrt(2.0 * np.log(node.visits) / child.visits)
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
        while not node.children == []:
            node = node.get_next_state()
        return node.reward_fct(self.joueur)

    def backup(self, node, reward):
        while node is not None:
            node.visits += 1
            if node.joueur == self.joueur:
                reward = -reward
            else:
                reward = reward
            node.reward += reward
            node = node.parent

    def __init__(self, grille):
        self.grille = grille
        self.joueur = 1

    def jouer_puissance4(self):
        while not self.grille.fin_jeu:
            self.grille.afficher_grille()
            # time.sleep(1)
            # Demande à l'utilisateur de choisir la colonne
            if self.grille.joueur_actuel == 1:
                self.joueur = 1
                self.grille.placer_jeton(self.utcsearch(self.grille, 1))
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
