
from alphabeta import alpha_beta
from minmax import minmax
from mcts import mcts
from puissance4 import puissance4

total = 0
maxxxx = 50
for i in range(maxxxx):
    jeu = puissance4()
    iaaa = alpha_beta(jeu, 3)
    total += iaaa.jouer_puissance4()
    print(i)
print("Nombre de fois où l'IA gagne contre l'aléatoire :", total, "/", maxxxx)
# jeu.jouer_puissance4()
# jeu = Puissance4()
# iaaaaa = AlphaBeta(jeu, 4)
# iaaaaa.jouer_puissance4()
