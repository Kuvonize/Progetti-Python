#Flower Shop Ordering To Go - Create a flower shop application which deals 
#in flower objects and use those flower objects in a bouquet object which can then be sold. 
# Keep track of the number of objects and when you may need to order more.

from class_flower import Flower
from class_bouquet import Bouquet
from class_inventario import Inventario

inventario=Inventario()
rosa1=Flower('rosa','rosso',5,20)
rosa2=Flower('rosa','bianco',5,17)
rosa3=Flower('rosa','blu',6,15)
girasole=Flower('girasole','giallo',8,18)
margherita=Flower('margherita','bianco',1,40)
tulipano1=Flower('tulipano','rosso',4,14)
tulipano2=Flower('tulipano','giallo',4,14)
tulipano3=Flower('tulipano','viola',5,14)
lista_fiori=[rosa1,rosa2,rosa3,girasole,margherita,tulipano1,tulipano2,tulipano3]
for fiore in lista_fiori:
    inventario.aggiungi_fiore(fiore)

print(inventario)
rosa_rossa=inventario.cerca_fiore('rosa','rosso')
tulipano_giallo=inventario.cerca_fiore('tulipano','giallo')
girasole_giallo=inventario.cerca_fiore('girasole','giallo')
dizionario_fiori={rosa_rossa:3,tulipano_giallo:2,girasole_giallo:1}

bouquet1=Bouquet('Romantic Mix',dizionario_fiori)

if bouquet1.verifica_disponibilita():
    bouquet1.consuma_fiori()
    print(bouquet1)
else:
    print('Attenzione: non si sono abbastanza fiori per comporre il bouquet!')

da_riordinare=inventario.fiori_da_riordinare(15)
if len(da_riordinare)>0:
    for fiore in da_riordinare:
        print(fiore)
else:
    print('Hai ancora abbastanza fiori a disposizione')    

