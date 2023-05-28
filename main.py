from jouer import jouer

if __name__ == '__main__':
    total = 0
    maxxxx = 10
    jeu = jouer()
    for i in range(maxxxx):
        total += jeu.jouer_puissance4()
        print(i)
    print("Nombre de victoire du joueur 1 :", total, "/", maxxxx)
    print("Nombre de victoire du joueur 2 :", maxxxx - total, "/", maxxxx)
