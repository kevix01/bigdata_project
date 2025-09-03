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

def stampa_itemset_frequenti_nomi(itemset_freq, mappatura_inversa, nome_file):
    f=open(nome_file,"w")
    itemset_freq_nomi = []
    f.write("Itemset frequenti:\n")
    k=1
    f.write("Itemset di livello 1:\n")
    for itemset in itemset_freq:
        if len(itemset)>k:
            k+=1
            f.write(f"Itemset di livello {k}:\n")
        itemlist=list(itemset)
        itemset_nomi = [mappatura_inversa[i] for i in itemlist]
        f.write(str(itemset_nomi)+"\n")
        itemset_freq_nomi.append(itemset_nomi)
    f.write("\n")
    f.close()
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
    print("\nEsecuzione algoritmo A-priori")
    itemset_freq_a_priori, _, _ = a_priori_algorithm(lista_transazioniID, 400)
    print(itemset_freq_a_priori)
    # STAMPA RISULTATI TOIVONEN SU FILE
    itemset_freq_a_priori_nomi = stampa_itemset_frequenti_nomi(itemset_freq_a_priori, mappatura_inversa, "Risultati_A_priori.txt")
    #print(itemset_freq_a_priori_nomi)


    # ESECUZIONE DELL'ALGORITMO DI TOIVONEN
    print("\nEsecuzione algoritmo Toivonen")
    sorted_frequent_itemset=toivonen_algorithm(lista_transazioniID, 400, 0.5)

    # STAMPA RISULTATI TOIVONEN SU FILE
    stampa_itemset_frequenti_nomi(sorted_frequent_itemset,mappatura_inversa,"Risultati_Toivonen.txt")



