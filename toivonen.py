import random
from itertools import combinations
from a_priori import *

# FUNZIONE CREAZIONE NEGATIVE BORDER
def negative_border_itemset(itemsets_frequenti, itemsets_candidati):
    # calcolo degli itemset non frequenti all'interno del campione
    infrequent = itemsets_candidati - itemsets_frequenti
    neg_border = set()

    for itemset in infrequent:
        # controlla che tutti i sottoinsiemi immediati siano frequenti
        all_subsets_frequent = all(
            frozenset(subset) in itemsets_frequenti
            for subset in combinations(itemset, len(itemset) - 1)
        )
        if all_subsets_frequent:
            neg_border.add(itemset)
    
    return neg_border

   
def toivonen_algorithm(lista_basketsID,soglia,frazione_campioni):
    while True:
        # CAMPIONAMENTO
        k = int(len(lista_basketsID) * frazione_campioni) #numero di campioni
        campione = random.sample(lista_basketsID, k) #lista di baskets estratti

        # CALCOLO DEL SUPPORTO EFFETTIVO
        supporto = soglia*frazione_campioni*0.8

        # ESECUZIONE ALGORITMO A-PRIORI SUL CAMPIONE
        print("Esecuzione algoritmo a-priori sul campione")
        _, set_itemsets_frequenti, set_itemsets_candidati = a_priori_algorithm(campione,supporto)

        # CREAZIONE NEGATIVE BORDER
        negative_border = negative_border_itemset(set_itemsets_frequenti, set_itemsets_candidati)

        # UNIONE ITEMSET FREQUENTI NEL CAMPIONE E ITEMSET DEL NEGATIVE BORDER
        set_unione_frequenti_negative = set_itemsets_frequenti.union(negative_border)

        # CONTEGGIO ITEMSET OTTENUTI NELL'INTERO DATASET
        set_itemsets_freq_full_dataset = set()
        print("\nConteggio itemset nel dataset completo")
        for k in [1,2,3]:
            # divisione degli itemset per dimensione e conteggio nel dataset completo
            itemsets_size_k = {itemset for itemset in set_unione_frequenti_negative if len(itemset) == k}
            print(f"Inizio conteggio itemset di dimensione {k}...")
            set_itemsets_freq_full_dataset.update(filterCandidates(itemsets_size_k, lista_basketsID, soglia, k))

        # VERIFICA PRESENZA ITEMSET DEL NEGATIVE BORDER NEL SET DI ITEMSET FREQUENTI TROVATI NEL FULL DATASET
        found_frequent_in_border = False
        for itemset in negative_border:
            if itemset in set_itemsets_freq_full_dataset:
                print(f"!!! FALLIMENTO: un elemento del negative border è risultato frequente.")
                print("L'algoritmo viene eseguito su un nuovo campione.")
                found_frequent_in_border = True
                break 
        
        # Se il ciclo for è terminato senza trovare itemset del negative border tra quelli frequenti, il campione era valido.
        if not found_frequent_in_border:
            print("\nSUCCESSO: Il campione era rappresentativo. Nessun itemset del negative border è risultato frequente.")
            break 
        
    # CREAZIONE LISTA FINALE DI ITEMSET FREQUENTI - selezione degli itemset frequenti nel campione scelto
    lista_itemsets_finale=[]
    for itemset in set_itemsets_frequenti:
        if itemset in set_itemsets_freq_full_dataset:
            lista_itemsets_finale.append(itemset)

    # ORDINAMENTO LISTA
    sorted_itemsets = sorted(lista_itemsets_finale,key=len)
    return sorted_itemsets