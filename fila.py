class Fila:

    #quando o cara não preenche a capacidade ela é infinita
    def __init__(self,chegada,atend,servidores,capacidade=-1):
        self.chegada = chegada
        self.atend = atend
        self.servidores = servidores
        self.capacidade = capacidade
