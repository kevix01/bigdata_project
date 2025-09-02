import random
from a_priori import a_priori_algorithm

def toivonen_algorithm(lista_transazioniID,soglia,frazione_campioni):
    # CAMPIONAMENTO
    k = int(len(lista_transazioniID) * frazione_campioni) #numero di campioni
    campione = random.sample(lista_transazioniID, k) #lista di transazioni estratte

    #print(len(campione))

    # CALCOLO DELLA SOGLIA
    supporto = soglia*frazione_campioni

    # ESECUZIONE ALGORITMO A-PRIORI SUL CAMPIONE
    lista_itemset_freq_campione=a_priori_algorithm(campione,supporto)
    print(lista_itemset_freq_campione)