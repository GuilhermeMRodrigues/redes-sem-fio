import time
import copy
from camadaFisica import CamadaFisica
import logging
import numpy as np

class CamadaLink(CamadaFisica):
    def mac(obj, pacote, nos):
        while(True):
            busyToneVizinhos = 0
            for vizinho in nos[pacote.header_mac[0]].vizinhos:
                if nos[vizinho.id].busy_tone:
                    busyToneVizinhos = 1
                    
            if busyToneVizinhos:
                time.sleep(np.random.random_sample())
            else:
                for vizinho in nos[pacote.header_mac[0]].vizinhos:
                    envia_pacote = copy.deepcopy(pacote)
                    envia_pacote.no_receptor = vizinho.id
                    nos[pacote.header_mac[0]].enviaLink(envia_pacote, nos)
                break
        pass

    def enviaLink(obj, pacote, nos):
        nos[pacote.no_receptor].busy_tone = True
        super().envia(pacote, nos)
        pass

    def recebeLink(obj, pacote, nos):
        nos[pacote.no_receptor].busy_tone = False
        if(pacote.no_receptor == pacote.header_mac[1] or (pacote.header_mac[1] == -1)):
            nos[pacote.no_receptor].redeReceptora(pacote, nos)
        pass

    