from camadaLink import CamadaLink
from scipy.spatial import distance
import pacotes 
import copy
import logging

class Rede(CamadaLink):
    def encontrarVizinhos(obj, id, nos):
        for no in nos:
            if(distance.seuclidean(nos[id].posicao, no.posicao, [1,1]) <= 1.5) and (nos[id].posicao is not no.posicao):
                nos[id].vizinhos.append(no)
            pass

    def redeEnvia(obj, pacote, nos):
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
    
    def redeRecebe(obj, pacote, nos):
        logging.info("Pacote["+str(pacote.id)+"]["+str(pacote.tipo_pacote)+"] dado:["+str(pacote.mensagem)+"] originario do nó "+str(pacote.header_mac[0])+" recebido pelo nó "+str(pacote.no_receptor))
    
        if(pacote.tipo_pacote == "DATA"):
            if(pacote.no_receptor == pacote.header_ip[1]):
                logging.info("Pacote["+str(pacote.id)+"]["+str(pacote.tipo_pacote)+"]chegou ao destino final "+str(pacote.no_receptor))
                pass                                                                              #pacote de dado chegou ao destino final
            else:
                nos[pacote.no_receptor].redeEnvia(pacote, nos)

        if((pacote.tipo_pacote == "RREQ") and not(pacote.id in nos[pacote.no_receptor].rreq_buffer)):
            nos[pacote.no_receptor].rreq_buffer.append(pacote.id)
            pacote_copia = copy.deepcopy(pacote)
            pacote_copia.mensagem.append(pacote.no_receptor) #MENSAGEM RECEBENDO NO?
            mensagem_copia = copy.deepcopy(pacote_copia.mensagem)
            nos[pacote.no_receptor].fillTable(nos, pacote_copia)
            if(pacote.no_receptor == pacote.header_ip[1]):  #se o no receptor for igual ao no de destino envia ao vizinho que enviou a request um pacote RREP
                mensagem_copia.reverse() #reverte ordem dos indices RREP
                rrep = pacotes.Pacotes(pacote.id, pacote.header_ip[1], pacote.header_ip[0], mensagem_copia, "RREP") #envia o caminho reverso RREP
                rrep.dsr = copy.deepcopy(mensagem_copia)
                nos[pacote.no_receptor].redeEnvia(rrep, nos)                                          #envia rrep
            else:
                pacote_copia.header_mac = [pacote.no_receptor, -1]
                nos[pacote.no_receptor].rreq_buffer.append(pacote.id)
                super().mac(pacote_copia, nos)                                         #reenvia rreq
                
        if(pacote.tipo_pacote == "RREP" and not(pacote.id in nos[pacote.no_receptor].rrep_buffer)):
            nos[pacote.no_receptor].fillTable(nos, pacote) #
            nos[pacote.no_receptor].rrep_buffer.append(pacote.id)
            if(pacote.no_receptor == pacote.header_ip[1]):
                pass                                                                              #apos a execuçao do dsr, eniva o pacote inicial que está no buffer
            else:
                nos[pacote.no_receptor].redeEnvia(pacote, nos)                                           #reenvia rrep
        pass

    def requisicaoRota(obj, nos, pacote):
        mensagem = [pacote.header_ip[0]]
        pacote.Pacotes.id_rreq = pacote.Pacotes.id_rreq + 1
        rreq = pacote.Pacotes(pacote.Pacotes.id_rreq, pacote.header_ip[0], pacote.header_ip[1], mensagem, "RREQ")
        nos[pacote.header_ip[0]].rreq_buffer.append(rreq.id)
        super().mac(rreq, nos)
        pass

    def preencheTabela(obj, nos, pacote):
        index_no = pacote.mensagem.index(nos[pacote.no_receptor].id)
        pacote_copia = copy.deepcopy(pacote.mensagem)

        caminhoEsquerda = pacote_copia[:index_no+1]
        caminhoEsquerda.reverse()
        if index_no != 0:
            for i in range(1, len(caminhoEsquerda)):
                if nos[pacote.no_receptor].routes.get(caminhoEsquerda[i]) is None:
                    nos[pacote.no_receptor].routes[caminhoEsquerda[i]] = caminhoEsquerda[:i+1]
                elif len(nos[pacote.no_receptor].routes[caminhoEsquerda[i]]) > len(caminhoEsquerda[:i+1]):
                    nos[pacote.no_receptor].routes[caminhoEsquerda[i]] = caminhoEsquerda[:i+1]

        caminhoDireita = pacote_copia[index_no:]
        if index_no != (len(pacote.data) - 1):
            for i in range(1,len(caminhoDireita)):
                if nos[pacote.rec_node].routes.get(caminhoDireita[i]) is None:
                    nos[pacote.rec_node].routes[caminhoDireita[i]] = caminhoDireita[:i+1]
                elif len(nos[pacote.rec_node].routes[caminhoDireita[i]]) > len(caminhoDireita[:i+1]):
                    nos[pacote.rec_node].routes[caminhoDireita[i]] = caminhoDireita[:i+1]        

        logging.info("Rotas do nó "+str(pacote.rec_node)+": "+str(nos[pacote.rec_node].routes))
        pass
