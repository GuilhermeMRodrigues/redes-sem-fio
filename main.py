import pacotes
import roteador as rot
import numpy as np

id = 0
nos = []

for x in range(3):
    for y in range(3):
        nos.append(rot.Roteador(id, x, y))
        id = id + 1

nos = np.array(nos)

pacote = pacotes.Pacotes(0, 0, 4, [1,2,2,1,1], "DATA")
pacote2 = pacotes.Pacotes(3, 4, 0, [1,2,1,2,1], "DATA")

for i in nos:
    i.encontrarVizinhos(i.id, nos)

nos[0].redeEnvia(pacote, nos)
nos[2].redeEnvia(pacote2, nos)

