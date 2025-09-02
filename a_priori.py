from itertools import combinations
from multiprocessing import Pool, cpu_count


""" baskets = [{1,2,4,5,7},{1,2,6},{1,4,6,7},{3,5,6},{1,2,4,7}]
minSup = 3 """

# compute the unions of pairs of itemsets with k elements
def getUnion(itemSet,k):
    return set([i.union(j) for i in itemSet for j in itemSet if len(i.union(j))==k])

def process_basket(args):
    idx, b, candidateSet, k, total = args
    local_count = {}
    for s in combinations(b, k):
        fs = frozenset(s)
        if fs in candidateSet:
            local_count[fs] = local_count.get(fs, 0) + 1

    # stampa progressiva
    #print(f"[Process] Basket {idx+1}/{total} completato")

    return local_count

def filterCandidates(candidateSet, baskets, minSup, k):
    total = len(baskets)
    # includo l'indice per poter stampare progressivamente
    tasks = [(i, b, candidateSet, k, total) for i, b in enumerate(baskets)]

    with Pool(cpu_count()) as pool:
        results = pool.map(process_basket, tasks)

    # riduzione dei conteggi
    count = {}
    for local_count in results:
        for item, v in local_count.items():
            count[item] = count.get(item, 0) + v

    #print("[Main] Tutti i basket sono stati elaborati.")
    return {item for item, v in count.items() if v >= minSup}

""" # select frequent items
def filterCandidates(candidateSet,baskets,minSup,k):
    count = dict()
    counter = 0
    for b in baskets:
        # create all subsets of size k from basket
        subsets = list(combinations(b,k))
        for s in subsets:
            # update counter is itemset is a candidate set
            if frozenset(s) in candidateSet:
                try:
                    count[frozenset(s)] +=1
                except KeyError:
                    count[frozenset(s)] = 1
        counter += 1
        if (k == 3) and (counter % 100 == 0):
            print(counter)
    # return the set of itemsets with count equal or above the threshold
    return {k for k,v in count.items() if v >= minSup} """


def a_priori_algorithm(baskets, minSup):
    # get frequent items (pass 1)
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

    #print("L1 item set: "+str(L1ItemSet))

    # pass 2,...,k
    currentLSet = L1ItemSet
    frequentItemsets = currentLSet
    allFrequentItemsets = [currentLSet]
    set_candidate_itemsets = set()
    k = 2

    while currentLSet and k <=3 :
        # create candidate set from k-1 frequent itemsets
        print("Generazione set candidati di dimensione "+str(k))
        candidateSet = getUnion(currentLSet,k)
        set_candidate_itemsets.update(candidateSet)
        # filter itemsets by frequency
        print("Filtraggio set candidati...")
        currentLSet = filterCandidates(candidateSet,baskets,minSup,k)
        
        # add frequent itemsets of size k to the frequent itemset
        frequentItemsets=frequentItemsets.union(currentLSet)
        allFrequentItemsets.append(currentLSet)
        #print(currentLSet)
        #break
        k += 1

    #print(frequentItemsets)
    return allFrequentItemsets, frequentItemsets, set_candidate_itemsets
