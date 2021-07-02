class Roteador():
    def __init__(obj, id, posX, posY):
        obj.id = id
        obj.posicao = [posX, posY]
        obj.vizinhos = []
        obj.rotas = {obj.id:obj.id}
        obj.busy_tone = False
        obj.rreq_buffer = [] #processo de descoberta de rotas atraves da inundacao de pacotes do tipo route requests (rreq)    
        obj.rrep_buffer = [] #
        pass
    