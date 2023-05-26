from alphabeta import alpha_beta
from minmax import minmax
from mcts import mcts
from puissance4 import puissance4

total = 0
maxxxx = 1
for i in range(maxxxx):
    jeu = puissance4()
    iaaa = mcts(jeu, 1)
    total += iaaa.jouer_puissance4()
    print(i)
print("Nombre de fois où l'IA gagne contre l'aléatoire :", total, "/", maxxxx)
