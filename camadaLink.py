import time
import copy
from camadaFisica import CamadaFisica
import numpy as np

class CamadaLink(CamadaFisica):

    def mac(obj, pacote, nos):
        while(True):
            busyToneVizinhos = 0
            for vizinho in nos[pacote.header_mac[0]].vizinhos:
                    busyToneVizinhos += nos[vizinho.id].busy_tone
                    
            if busyToneVizinhos > 0:
                print("_____________no ocupado________________")
                time.sleep(np.random.random_sample())
            else:
                for vizinho in nos[pacote.header_mac[0]].vizinhos:
                    envia_pacote = copy.deepcopy(pacote)
                    envia_pacote.no_receptor = vizinho.id
                    nos[pacote.header_mac[0]].enviaLink(envia_pacote, nos)
                break
        pass

    def enviaLink(obj, pacote, nos):
        nos[pacote.no_receptor].busy_tone = 1
        super().envia(pacote, nos)
        pass

    def recebeLink(obj, pacote, nos):
        nos[pacote.no_receptor].busy_tone = 0
        if(pacote.no_receptor == pacote.header_mac[1] or (pacote.header_mac[1] == -1)):
            nos[pacote.no_receptor].redeRecebe(pacote, nos)
        pass



