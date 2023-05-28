from alphabeta import alpha_beta
from jouer import jouer
from puissance4 import puissance4

total = 0
maxxxx = 10
jeu = jouer()
for i in range(maxxxx):
    total += jeu.jouer_puissance4()
    print(i)
print("Nombre de fois où le joueur 1 gagne contre le joueur 2 :", total, "/", maxxxx)
