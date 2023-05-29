import time

from jouer import jouer

if __name__ == '__main__':
    total = 0
    maxxxx = 20
    jeu = jouer()
    for i in range(maxxxx):
        start = time.time()
        total += jeu.jouer_puissance4()
        print(i)
        print("Temps d'execution :", time.time() - start)
    print("Nombre de victoire du joueur 1 :", total, "/", maxxxx)
    print("Nombre de victoire du joueur 2 :", maxxxx - total, "/", maxxxx)
