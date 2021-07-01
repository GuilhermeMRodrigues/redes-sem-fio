from camadaLink import CamadaLink
from scipy.spatial import distance
import pacotes as Pacotes
import copy
import logging

class Rede(CamadaLink):
    def encontrarVizinhos(obj, id, nos):
        for no in nos:
            if(distance.seuclidean(nos[id].posicao, no.posicao, [1,1]) <= 1.5) and (nos[id].posicao is not no.posicao):
                nos[id].vizinhos.append(no)
            pass

    def redeReceptora(obj, pacote, nos):
        envia_pacote = copy.deepcopy(pacote)
        if envia_pacote.dsr[0] == -1:
            if nos[envia_pacote.no_receptor].rotas.get(envia_pacote.header_ip[1]) is None:
                logging.info("Processo de descobrimento de rota iniciado pelo nó["+str(pacote.header_ip[0])+"] para o nó["+str(pacote.header_ip[1])+"]")
                nos[envia_pacote.no_receptor].requisicaoRota(nos, envia_pacote)
                envia_pacote.dsr = nos[envia_pacote.no_receptor].rotas.get(envia_pacote.header_ip[1])
            else:
                envia_pacote.dsr = nos[envia_pacote.no_receptor].rotas.get(envia_pacote.header_ip[1])
        envia_pacote.header_mac = [envia_pacote.dsr[0], envia_pacote.dsr[1]]
        envia_pacote.dsr.pop(0)
        super().mac(envia_pacote, nos)
        pass