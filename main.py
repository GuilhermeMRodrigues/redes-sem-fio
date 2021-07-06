import pacotes
import roteador as rot
import numpy as np

id = 0
nos = []

for x in range(2):
    for y in range(3):
        nos.append(rot.Roteador(id, x, y))
        id = id + 1
        
print("Quantidade de nos: ", id, "\n")

nos = np.array(nos)  

#id | origem | destino | mensagem | tipo
pacote = pacotes.Pacotes(9, 0, 3, "redes", "DATA")
pacote2 = pacotes.Pacotes(3, 1, 3, "sem", "DATA")
pacote3 = pacotes.Pacotes(10, 0, 3, "fio", "DATA")
pacote4 = pacotes.Pacotes(4, 2, 3, "bacana", "DATA")

for i in nos:
    i.encontrarVizinhos(i.id, nos)

nos[1].redeEnvia(pacote, nos)
nos[2].redeEnvia(pacote2, nos)  
nos[3].redeEnvia(pacote3, nos)
nos[4].redeEnvia(pacote4, nos)  

