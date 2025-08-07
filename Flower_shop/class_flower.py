class Flower():
    def __init__(self,nome,colore,prezzo,quantita_inventario):
        self.nome = nome
        self.colore = colore
        self.prezzo = prezzo
        self.quantita_inventario = quantita_inventario
    
    def riduci_quantita(self,quantita):
        self.quantita_inventario-=quantita

    def verifica_disponibilita(self,quantita):
        if quantita <= self.quantita_inventario:
            return True
        else:
            return False

    def da_riordinare(self,soglia):
        if self.quantita_inventario<soglia:
            return True
        else:
            return False

    def __str__(self):
        return f'Nome fiore: {self.nome} \n Colore: {self.colore} \n Prezzo: {self.prezzo} \n Quantità in inventario: {self.quantita_inventario}'           



