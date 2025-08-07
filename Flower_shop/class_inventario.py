from class_flower import Flower

class Inventario():
    def __init__(self):
        self.fiori={}

    def aggiungi_fiore(self,fiore):
        chiave=f'{fiore.nome.lower()}-{fiore.colore.lower()}'
        if chiave in self.fiori:
            self.fiori[chiave].quantita_inventario+=fiore.quantita_inventario
        else:
            self.fiori[chiave]=fiore

    def __str__(self):
        lista_fiori=''
        for fiore in self.fiori.values():
            lista_fiori+=str(fiore)+'\n'
        return f'Inventario: {lista_fiori}'    

    def fiori_da_riordinare(self,soglia):
        da_ordinare=[]
        for fiore in self.fiori.values():
            if fiore.da_riordinare(soglia):
                da_ordinare.append(fiore)
        return da_ordinare

    def cerca_fiore(self,nome,colore):
        chiave=f'{nome.lower()}-{colore.lower()}'
        return self.fiori.get(chiave,None)
                            
            




