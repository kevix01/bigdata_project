import pandas as pd
import re
import os
from a_priori import a_priori_algorithm
from toivonen import toivonen_algorithm


# Change the working directory to the directory containing the script
""" script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir) """

def crea_lista_transazioniID(transazioni, mappatura_item):
    lista_transazioniID=[]
    for tr in transazioni:
        lista_transazioniID.append([mappatura_item[item] for item in tr])
    return lista_transazioniID

def stampa_itemset_frequenti_nomi(itemset_freq, mappatura_inversa):
    itemset_freq_nomi = []
    print("Itemset frequenti:")
    k=1
    for livello in itemset_freq:
        print("Livello "+str(k))
        for itemset in livello:
            itemlist=list(itemset)
            itemset_nomi = [mappatura_inversa[i] for i in itemlist]
            print(itemset_nomi)
            itemset_freq_nomi.append(itemset_nomi)
        k+=1
        print("\n")
    return itemset_freq_nomi

if __name__ == "__main__":
    # LETTURA FILE CSV in un pandas dataframe
    df = pd.read_csv('archive/Assignment-1_Data.csv', sep=";")
    #print(df["Itemname"].tolist())


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
    """ print("Dimensioni dataframe dopo pulizia:", df_clean.shape) """


    # CREAZIONE LISTA ITEM (senza duplicati)
    lista_item = df_clean["Itemname"].drop_duplicates().tolist()
    """ print(len(lista_item))  # quanti item diversi ci sono
    print(lista_item)
    print(df_clean) """


    # CREAZIONE LISTA DELLE TRANSAZIONI
    # Raggruppiamo per BillNo e creiamo una lista degli Itemname per ogni transazione
    transazioni = df_clean.groupby("BillNo")["Itemname"].apply(list).tolist()
    # Mostriamo qualche esempio
    """ print("Esempi di transazioni:")
    for t in transazioni[:5]:
        print(t) """


    # CREAZIONE MAPPATURA ITEM → ID
    mappatura_item = {item: i for i, item in enumerate(lista_item)}
    """ print(mappatura_item[500]) """
    mappatura_inversa = {i: item for item, i in mappatura_item.items()}
    #print(mappatura_inversa[528])

    # CREAZIONE LISTA DELLE TRANSAZIONI CON INDICI DEGLI ITEM
    lista_transazioniID = crea_lista_transazioniID(transazioni, mappatura_item)
    #print(len(lista_transazioniID))


    # ESECUZIONE DELL'ALGORITMO A-PRIORI
    #itemset_freq_a_priori, _, _ = a_priori_algorithm(lista_transazioniID, 500)
    #print(itemset_freq_a_priori)
    #itemset_freq_a_priori_nomi = stampa_itemset_frequenti_nomi(itemset_freq_a_priori, mappatura_inversa)
    #print(itemset_freq_a_priori_nomi)


    # ESECUZIONE DELL'ALGORITMO DI TOIVONEN
    toivonen_algorithm(lista_transazioniID, 500, 0.05)



