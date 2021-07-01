class Pacotes():
    id_rrep = 0
    id_rreq = 0
    def __init__(obj, id, origem, destino, mensagem, tipo_pacote):
        obj.id = id
        obj.origem = origem
        obj.header_ip = [origem, destino]
        obj.header_mac = [origem, -1]
        obj.mensagem = mensagem
        obj.tipo_pacote = tipo_pacote
        obj.no_receptor = origem
        obj.dsr = [-1]
        pass
