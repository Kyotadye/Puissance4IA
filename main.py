from alphabeta import alpha_beta
from minmax import minmax
from mcts import mcts
from puissance4 import puissance4

total = 0
maxxxx = 10
for i in range(maxxxx):
    jeu = puissance4()
    #*jeu.jouer_puissance4()
    iaaa = mcts(jeu)
    total += iaaa.jouer_puissance4()
    print(i)
print("Nombre de fois où l'IA gagne contre l'aléatoire :", total, "/", maxxxx)
