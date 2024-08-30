from collections import Counter
from itertools import combinations
import math
import numpy as np
import pandas as pd
import function

watches =  pd.read_csv('watches.csv', sep=",")
data=watches.loc[:,["brand_names","Gender","Type"]]
data=data.to_numpy()
data=function.upper_matrice(data)
#PRETRAITEMENT
print("----------------------before----------------------")
print(data)
data=function.pretraitement1(data)
print("----------------------after----------------------")
print(data)
#FIN PRETRAITEMENT

itemset = []
for l in data:
    for i in l:
        if(i not in itemset ):
            itemset.append(i)
itemset = sorted(itemset)
print(itemset)

c = Counter()
occurrence = set()
for i in itemset:
    for d in data:
        if(i in d):
            c[i]+=1
    occurrence.add(c[i])

#calcule de minsup
s = function.minsup2(occurrence)
print(s)

print("C1:")
for i in c:
    print(str([i])+": "+str(c[i]))
print()

l = Counter()
for i in c:
    if(c[i] >= s):
        l[frozenset([i])]+=c[i]
print("L1:")
for i in l:
    print(str(list(i))+": "+str(l[i]))
print()
sl = l
taille = 1
rules=[]
for count in range (2,1000):
    nc = set()
    temp = list(l)

    #definer les fermetures
    close = {}
    for i in range(0,len(temp)):
        close[temp[i]] = temp[i]
        for j in range(0,len(temp)):
            k=0
            for q in data:
                qset = set(q)
                if(temp[i].issubset(qset) and temp[j].issubset(qset)):
                    k=k+1
            if(k==l[temp[i]]):
                close[temp[i]] = close[temp[i]].union(temp[j])

    print("------------les fermetures-----------")
    print(close)
    print("-------------------------------------")
    rules.append(function.close_regles(list(temp),close))

    for i in range(0,len(temp)):
        for j in range(i+1,len(temp)):
            t = temp[i].union(temp[j])
            if(len(t) == count):
                if(not t.issubset(close[temp[i]]) and not t.issubset(close[temp[j]])):
                    nc.add(t)
    nc = list(nc)
    c = Counter()
    for i in nc:
        c[i] = 0
        for q in data:
            temp = set(q)
            if(i.issubset(temp)):
                c[i]+=1
    print("C"+str(count)+":")
    for i in c:
        print(str(list(i))+": "+str(c[i]))
    print()
    l = Counter()
    for i in c:
        if(c[i] >= s):
            l[i]+=c[i]
    print("L"+str(count)+":")
    for i in l:
        print(str(list(i))+": "+str(l[i]))
    print()
    if(len(l) == 0):
        break
    sl = l
    taille = count
print("Final itemset: ")
print("L"+str(taille)+":")
for i in sl:
    print(str(list(i))+": "+str(sl[i]))
print()
print("------------les regles d'assosiation-----------")
print(rules)
print("-------------------------------------")


