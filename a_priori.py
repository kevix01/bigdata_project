from itertools import combinations

""" baskets = [{1,2,4,5,7},{1,2,6},{1,4,6,7},{3,5,6},{1,2,4,7}]
minSup = 3 """

# compute the unions of pairs of itemsets with k elements
def getUnion(itemSet,k):
    return set([i.union(j) for i in itemSet for j in itemSet if len(i.union(j))==k])

# select frequent items
def filterCandidates(candidateSet,baskets,minSup,k):
    count = dict()
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
    # return the set of itemsets with count equal or above the threshold
    return {k for k,v in count.items() if v >= minSup}


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
    k = 2

    while currentLSet and k<=3:
        # create candidate set from k-1 frequent itemsets
        print("Generazione set candidati di dimensione "+str(k))
        candidateSet = getUnion(currentLSet,k)
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
    return allFrequentItemsets