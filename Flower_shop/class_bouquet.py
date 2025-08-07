from class_flower import Flower
class Bouquet():
    def __init__(self,nome,fiori_quantita):
        self.nome=nome
        self.fiori_quantita=fiori_quantita
        

    def calcola_prezzo(self):
        totale=0
        if not self.fiori_quantita:
            return 0
        for fiore, quantita in self.fiori_quantita.items():
            totale+=(fiore.prezzo*quantita)
        return totale

    def verifica_disponibilita(self):
        for fiore, quantita in self.fiori_quantita.items():
            if not fiore.verifica_disponibilita(quantita):
                return False
        return True 

    def  consuma_fiori(self):
        for fiore, quantita in self.fiori_quantita.items():
            fiore.riduci_quantita(quantita)

    def __str__(self):
        risultato=f'Nome Bouquet: {self.nome}\n'
        risultato+='Composizione:\n'
        for fiore, quantita in self.fiori_quantita.items():
            risultato+=f'- {quantita} {fiore.nome} {fiore.colore}\n'
        risultato+=f'Costo Totale del Bouquet: €{self.calcola_prezzo():.2f}'
        return risultato+'\n'             
                 

        