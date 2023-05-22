import numpy as np

# Définition des constantes
TAILLE_GRILLE = (6, 7)  # Taille de la grille de jeu

# Création de la grille vide
grille = np.zeros(TAILLE_GRILLE, dtype=int)


# Fonction pour afficher la grille
def afficher_grille(grille):
    for row in grille:
        for cell in row:
            if cell == 0:
                print(".", end=" ")
            elif cell == 1:
                print("X", end=" ")
            else:
                print("O", end=" ")
        print()
    print()


# Fonction pour placer un jeton dans la colonne choisie
def placer_jeton(grille, colonne, joueur):
    for i in range(TAILLE_GRILLE[0] - 1, -1, -1):
        if grille[i][colonne] == 0:
            grille[i][colonne] = joueur
            break


# Fonction pour vérifier si un joueur a gagné
def verif_victoire(grille, joueur):
    # Vérification des lignes
    for i in range(TAILLE_GRILLE[0]):
        for j in range(TAILLE_GRILLE[1] - 3):
            if np.all(grille[i, j:j + 4] == joueur):
                return True

    # Vérification des colonnes
    for i in range(TAILLE_GRILLE[0] - 3):
        for j in range(TAILLE_GRILLE[1]):
            if np.all(grille[i:i + 4, j] == joueur):
                return True

    # Vérification des diagonales ascendantes
    for i in range(TAILLE_GRILLE[0] - 3):
        for j in range(TAILLE_GRILLE[1] - 3):
            if np.all(np.diag(grille[i:i + 4, j:j + 4]) == joueur):
                return True

    # Vérification des diagonales descendantes
    for i in range(TAILLE_GRILLE[0] - 3):
        for j in range(TAILLE_GRILLE[1] - 3):
            if np.all(np.diag(np.fliplr(grille[i:i + 4, j:j + 4])) == joueur):
                return True

    return False


# Fonction principale pour jouer au Puissance 4
def jouer_puissance4():
    joueur_actuel = 1
    nb_coups = 0
    fin_jeu = False

    while not fin_jeu:
        afficher_grille(grille)

        # Demande à l'utilisateur de choisir la colonne
        if joueur_actuel == 1:
            colonne = int(input("Joueur 1, choisissez la colonne (0-6) : "))
        else:
            colonne = int(input("Joueur 2, choisissez la colonne (0-6) : "))

        placer_jeton(grille, colonne, joueur_actuel)
        nb_coups += 1

        if verif_victoire(grille, joueur_actuel):
            afficher_grille(grille)
            if joueur_actuel == 1:
                print("Joueur 1 a gagné !")
            else:
                print("Joueur 2 a gagné !")
            fin_jeu = True
        elif nb_coups == TAILLE_GRILLE[0] * TAILLE_GRILLE[1]:
            afficher_grille(grille)
            print("Match nul !")
            fin_jeu = True

        # Changer de joueur
        joueur_actuel = 3 - joueur_actuel


# Lancer le jeu
jouer_puissance4()
