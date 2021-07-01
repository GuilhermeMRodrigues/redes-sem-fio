class Roteador():
    def __init__(obj, id, posX, posY):
        obj.id = id
        obj.posicao = [posX, posY]
        obj.vizinhos = []
        obj.rotas = {obj.id:obj.id}
        obj.busy_tone = False
        obj.rreq_buffer = []
        obj.rrep_buffer = []
        pass
    