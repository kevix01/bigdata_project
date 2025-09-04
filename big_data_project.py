import pandas as pd
import re
import os
from a_priori import a_priori_algorithm
from toivonen import toivonen_algorithm


def crea_lista_basketID(baskets, mappatura_item):
    lista_basketID=[]
    for tr in baskets:
        lista_basketID.append([mappatura_item[item] for item in tr])
    return lista_basketID

def stampa_itemset_frequenti_nomi(lista_itemset_freq, mappatura_inversa, nome_file):
    f=open(nome_file,"w")
    lista_itemset_freq_nomi = []
    f.write("Itemset frequenti:\n")
    k=1
    f.write("Itemset di livello 1:\n")
    for itemset in lista_itemset_freq:
        if len(itemset)>k:
            k+=1
            f.write(f"Itemset di livello {k}:\n")
        itemlist=list(itemset)
        lista_nomi_itemset = [mappatura_inversa[i] for i in itemlist]
        f.write(str(lista_nomi_itemset)+"\n")
        lista_itemset_freq_nomi.append(lista_nomi_itemset)
    f.write("\n")
    f.close()
    return lista_itemset_freq_nomi

if __name__ == "__main__":
    # LETTURA FILE CSV in un pandas dataframe
    df = pd.read_csv('archive/Assignment-1_Data.csv', sep=";", low_memory=False)


    # PULIZIA DEL DATASET
    # Lasciamo solo le colonne "BillNo" e "Itemname"
    df_clean = df[["BillNo", "Itemname"]]
    # Togliamo righe con valori mancanti
    df_clean = df_clean.dropna()
    # Creiamo un filtro per eliminare caratteri speciali  ^[A-Z0-9 ]+$ → solo lettere maiuscole, numeri, spazi e caratteri speciali
    mask_no_specials = df_clean["Itemname"].str.match(r'^[A-Z0-9 .,+\-!&/\'\\|":%&$_*]+$', na=False)
    # Creiamo un filtro per stringhe tutte maiuscole
    mask_upper = df_clean["Itemname"].str.isupper()
    # Applichiamo entrambe le condizioni
    df_clean = df_clean[mask_no_specials & mask_upper]


    # CREAZIONE LISTA ITEM (senza duplicati)
    lista_item = df_clean["Itemname"].drop_duplicates().tolist()


    # CREAZIONE LISTA DEI BASKET
    # Raggruppiamo per BillNo e creiamo una lista degli Itemname per ogni basket
    baskets = df_clean.groupby("BillNo")["Itemname"].apply(list).tolist()


    # CREAZIONE MAPPATURA ITEM → ID E MAPPATURA INVERSA
    mappatura_item = {item: i for i, item in enumerate(lista_item)}
    mappatura_inversa = {i: item for item, i in mappatura_item.items()}


    # CREAZIONE LISTA DELLE TRANSAZIONI CON INDICI DEGLI ITEM
    lista_basketsID = crea_lista_basketID(baskets, mappatura_item)


    # ESECUZIONE DELL'ALGORITMO A-PRIORI
    print("Esecuzione algoritmo A-priori")
    lista_itemset_freq_a_priori, _, _ = a_priori_algorithm(lista_basketsID, 400)
    # STAMPA RISULTATI A-PRIORI SU FILE
    stampa_itemset_frequenti_nomi(lista_itemset_freq_a_priori, mappatura_inversa, "Risultati_A_priori.txt")


    # ESECUZIONE DELL'ALGORITMO DI TOIVONEN
    print("\nEsecuzione algoritmo Toivonen")
    lista_itemset_freq_toivonen = toivonen_algorithm(lista_basketsID, 400, 0.3)

    # STAMPA RISULTATI TOIVONEN SU FILE
    stampa_itemset_frequenti_nomi(lista_itemset_freq_toivonen,mappatura_inversa,"Risultati_Toivonen.txt")