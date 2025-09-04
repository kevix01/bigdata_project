from itertools import combinations
from multiprocessing import Pool, cpu_count

# Calcolo dell'unione delle coppie di itemsets con k elementi
def getUnion(itemSet,k):
    return set([i.union(j) for i in itemSet for j in itemSet if len(i.union(j))==k])

# Funzione per processare il singolo basket
def process_basket(args):
    b, candidateSet, k = args
    local_count = {}
    for s in combinations(b, k):
        fs = frozenset(s)
        if fs in candidateSet:
            local_count[fs] = local_count.get(fs, 0) + 1

    return local_count

# Selezione degli itemset frequenti
def filterCandidates(candidateSet, baskets, minSup, k):
    # associazione di un basket per ogni task
    tasks = [(b, candidateSet, k) for b in baskets]

    # mappatura della funione process_basket al singolo task
    with Pool(cpu_count()) as pool:
        results = pool.map(process_basket, tasks)

    # riduzione dei conteggi ehhettuati dai singoli task
    count = {}
    for local_count in results:
        for item, v in local_count.items():
            count[item] = count.get(item, 0) + v

    return {item for item, v in count.items() if v >= minSup}


def a_priori_algorithm(baskets, minSup):
    # Calcolo item frequenti (passo 1)
    C1ItemSet = dict()
    for b in baskets:
        for item in b:
            try:
                C1ItemSet[item] += 1
            except KeyError:
                C1ItemSet[item] = 1

    L1ItemSet = set()
    for key,value in C1ItemSet.items():
        if value>=minSup:
            L1ItemSet.add(frozenset({key}))

    # passi 2,...,k
    currentLSet = L1ItemSet
    set_frequent_itemsets = currentLSet
    
    list_itemset_freq = []
    list_itemset_freq.extend(currentLSet)
    set_candidate_itemsets = set()
    k = 2

    while currentLSet and k <=3 :
        # creazione degli itemset candidati a partire dagli itemset frequenti di dimensione k-1
        print("Generazione set candidati di dimensione "+str(k)+"...")
        candidateSet = getUnion(currentLSet,k)
        set_candidate_itemsets.update(candidateSet)
        # filtraggio degli itemset in base alla loro frequenza
        print("Filtraggio set candidati...")
        currentLSet = filterCandidates(candidateSet,baskets,minSup,k)
        
        # aggiunta itemset frequenti di dimensione k agli itemset frequenti
        set_frequent_itemsets=set_frequent_itemsets.union(currentLSet)
        list_itemset_freq.extend(currentLSet)
        k += 1

    return list_itemset_freq, set_frequent_itemsets, set_candidate_itemsets
