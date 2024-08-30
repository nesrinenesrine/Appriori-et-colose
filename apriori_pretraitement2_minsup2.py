from collections import Counter
from itertools import combinations
import pandas as pd
import function

watches =  pd.read_csv('watches.csv', sep=",")
data=watches.loc[:,["brand_names","Gender","Type"]]
data=data.to_numpy()
data=function.upper_matrice(data)
data=function.pretraitement2(data)

itemset = []
for l in data:
    for i in l:
        if(i not in itemset ):
            itemset.append(i)
itemset = sorted(itemset)

c = Counter()
occurrence = set()
for i in itemset:
    for d in data:
        if(i in d):
            c[i]+=1
    occurrence.add(c[i])

s=function.minsup2(occurrence)
pl=function.aprpri(data,itemset,s)

regle=function.regle(data,pl)
#prendre les regles avec la conficance sup a 60% et lift diff de 1 on utilisant la fonction 'fonction'
x=function.fonction(regle)

