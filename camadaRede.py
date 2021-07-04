from camadaLink import CamadaLink
from scipy.spatial import distance
import pacotes 
import copy

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
                print("Inciando broadcast para todos os vizinhos diretos a partir do no origem: ["+str(pacote.header_ip[0])+"] para o no destino: ["+str(pacote.header_ip[1])+"]")
                nos[envia_pacote.no_receptor].requisicaoRota(nos, envia_pacote)
                envia_pacote.dsr = nos[envia_pacote.no_receptor].rotas.get(envia_pacote.header_ip[1])
            else:
                envia_pacote.dsr = nos[envia_pacote.no_receptor].rotas.get(envia_pacote.header_ip[1])
        envia_pacote.header_mac = [envia_pacote.dsr[0], envia_pacote.dsr[1]]
        envia_pacote.dsr.pop(0)
        super().mac(envia_pacote, nos)
        pass
    
    def redeRecebe(obj, pacote, nos):
        print("\nPacote["+str(pacote.id)+"]["+str(pacote.tipo_pacote)+"] mensagem:["+str(pacote.mensagem)+"] originario do no "+str(pacote.header_mac[0])+" recebido pelo no "+str(pacote.no_receptor))
    
        if(pacote.tipo_pacote == "DATA"):
            if(pacote.no_receptor == pacote.header_ip[1]):
                print("\nPacote["+str(pacote.id)+"]["+str(pacote.tipo_pacote)+"]chegou ao destino final "+str(pacote.no_receptor))
                pass                                                                              
            else:
                nos[pacote.no_receptor].redeEnvia(pacote, nos)

        if((pacote.tipo_pacote == "RREQ") and not(pacote.id in nos[pacote.no_receptor].rreq_buffer)):
            nos[pacote.no_receptor].rreq_buffer.append(pacote.id)
            pacote_copia = copy.deepcopy(pacote)
            pacote_copia.mensagem.append(pacote.no_receptor) 
            mensagem_copia = copy.deepcopy(pacote_copia.mensagem)
            nos[pacote.no_receptor].preencheTabela(nos, pacote_copia)
            if(pacote.no_receptor == pacote.header_ip[1]):  
                mensagem_copia.reverse() 
                rrep = pacotes.Pacotes(pacote.id, pacote.header_ip[1], pacote.header_ip[0], mensagem_copia, "RREP") 
                rrep.dsr = copy.deepcopy(mensagem_copia)
                nos[pacote.no_receptor].redeEnvia(rrep, nos)                                          
            else:
                pacote_copia.header_mac = [pacote.no_receptor, -1]
                nos[pacote.no_receptor].rreq_buffer.append(pacote.id)
                super().mac(pacote_copia, nos)                                         
                
        if(pacote.tipo_pacote == "RREP" and not(pacote.id in nos[pacote.no_receptor].rrep_buffer)):
            nos[pacote.no_receptor].preencheTabela(nos, pacote) #
            nos[pacote.no_receptor].rrep_buffer.append(pacote.id)
            if(pacote.no_receptor == pacote.header_ip[1]):
                pass                                                                              
            else:
                nos[pacote.no_receptor].redeEnvia(pacote, nos)                                           
        pass

    def requisicaoRota(obj, nos, pacote):
        mensagem = [pacote.header_ip[0]]
        pacotes.Pacotes.id_rreq = pacotes.Pacotes.id_rreq + 1
        rreq = pacotes.Pacotes(pacotes.Pacotes.id_rreq, pacote.header_ip[0], pacote.header_ip[1], mensagem, "RREQ")
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
                if nos[pacote.no_receptor].rotas.get(caminhoEsquerda[i]) is None:
                    nos[pacote.no_receptor].rotas[caminhoEsquerda[i]] = caminhoEsquerda[:i+1]
                elif len(nos[pacote.no_receptor].rotas[caminhoEsquerda[i]]) > len(caminhoEsquerda[:i+1]):
                    nos[pacote.no_receptor].rotas[caminhoEsquerda[i]] = caminhoEsquerda[:i+1]

        caminhoDireita = pacote_copia[index_no:]
        if index_no != (len(pacote.mensagem) - 1):
            for i in range(1,len(caminhoDireita)):
                if nos[pacote.no_receptor].rotas.get(caminhoDireita[i]) is None:
                    nos[pacote.no_receptor].rotas[caminhoDireita[i]] = caminhoDireita[:i+1]
                elif len(nos[pacote.no_receptor].rotas[caminhoDireita[i]]) > len(caminhoDireita[:i+1]):
                    nos[pacote.no_receptor].rotas[caminhoDireita[i]] = caminhoDireita[:i+1]        

        print("\nRotas do no "+str(pacote.no_receptor)+": "+str(nos[pacote.no_receptor].rotas))
        pass
