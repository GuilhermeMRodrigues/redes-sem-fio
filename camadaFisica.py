
class CamadaFisica():
    def envia(obj, pacote, nos):
        nos[pacote.no_receptor].recebe(pacote, nos)
        pass

    def recebe(obj, pacote, nos):
        nos[pacote.no_receptor].recebeLink(pacote, nos)
        pass