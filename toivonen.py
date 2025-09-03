import random
from itertools import combinations
from a_priori import *

#FUNZIONE CREAZIONE NEGATIVE BORDER
def negative_border_itemset(itemsets_frequenti, itemsets_candidati):
    
    infrequent = itemsets_candidati - itemsets_frequenti
    neg_border = set()


    for itemset in infrequent:
        # Controlla che tutti i sottoinsiemi immediati siano frequenti
        all_subsets_frequent = all(
            frozenset(subset) in itemsets_frequenti
            for subset in combinations(itemset, len(itemset) - 1)
        )
        if all_subsets_frequent:
            neg_border.add(itemset)
    
    return neg_border

   
def toivonen_algorithm(lista_transazioniID,soglia,frazione_campioni):
    while True:
        # CAMPIONAMENTO
        k = int(len(lista_transazioniID) * frazione_campioni) #numero di campioni
        campione = random.sample(lista_transazioniID, k) #lista di transazioni estratte

        #print(len(campione))

        # CALCOLO DELLA SOGLIA
        supporto = soglia*frazione_campioni*0.8

        # ESECUZIONE ALGORITMO A-PRIORI SUL CAMPIONE
        print("\nEsecuzione algoritmo a-priori sul campione...")
        lista_itemset_freq_campione, set_itemsets_frequenti, set_itemsets_candidati =a_priori_algorithm(campione,supporto)
        #print(lista_itemset_freq_campione)
        
        #CREAZIONE NEGATIVE BORDER
        negative_border = negative_border_itemset(set_itemsets_frequenti, set_itemsets_candidati)
        #print(f"ITEMSETS FREQUENTI: {set_itemsets_frequenti}\n")
        #print(f"ITEMSETS CANDIDATI: {set_itemsets_candidati}\n")
        #print(f"NEGATIVE BORDER: {negative_border}")

        
        set_unione_frequenti_negative = set_itemsets_frequenti.union(negative_border)


        
        itemsets_frequenti_full_dataset = set()

        print("\nConteggio itemset nel dataset completo")

        for k in [1,2,3]:
            print(f"Inizio conteggio itemset di dimensione {k}")
            itemsets_size_k = {itemset for itemset in set_unione_frequenti_negative if len(itemset) == k}
            itemsets_frequenti_full_dataset.update(filterCandidates(itemsets_size_k, lista_transazioniID, soglia, k))
        
        with open("full.txt", "w") as f:
            for s in itemsets_frequenti_full_dataset:
                f.write(str(s)+"\n")

        """ # VERIFICA PRESENZA DEGLI ITEMSET DEL NEGATIVE BORDER NEGLI ITEMSET FREQUENTI DEL FULL DATASET
        for itemset in itemsets_frequenti_full_dataset:
            if itemset in negative_border:
                print("\nEsecuzione dell'algoritmo di Toivonen su un nuovo campione...")
                toivonen_algorithm(lista_transazioniID,soglia,frazione_campioni) """

        found_frequent_in_border = False
        for itemset in negative_border:
            if itemset in itemsets_frequenti_full_dataset:
                print(f"!!! FALLIMENTO: L'itemset {itemset} della negative border è risultato frequente.")
                print("Il campione non era rappresentativo. Si riparte con un nuovo campione.")
                found_frequent_in_border = True
                break  # Non serve controllare gli altri, uno è sufficiente per fallire
        
        # Se il ciclo for è terminato senza trovare itemset della negative border
        # tra quelli frequenti, il campione era valido e possiamo uscire dal while.
        if not found_frequent_in_border:
            print("\nSUCCESSO: Il campione era rappresentativo. Nessun itemset della negative border è risultato frequente.")
            break # Esce dal ciclo while
        
    # CREAZIONE LISTA FINALE DI ITEMSET FREQUENTI
    lista_itemsets_finale=[]
    for itemset in set_itemsets_frequenti:
        if itemset in itemsets_frequenti_full_dataset:
            lista_itemsets_finale.append(itemset)

    # ORDINAMENTO LISTA
    sorted_itemsets = sorted(lista_itemsets_finale,key=len)
    return sorted_itemsets
    
