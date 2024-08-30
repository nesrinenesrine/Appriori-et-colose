from collections import Counter
from itertools import combinations
import math

def minsup1(itemset,data):
    c = Counter()
    for i in itemset:
        for d in data:
            if(i in d):
                c[i]+=1
    min=math.inf
    max=0
    for i in c:
        if(c[i]<min):
            min=c[i]
        elif(c[i]>max):
            max=c[i] 
    for i in c:
        c[i]=c[i]/(max-min)

    moyen=0
    for i in c:
        moyen=moyen+c[i]
    moyen=moyen/(len(c))

    variance=0
    for i in c:
        variance=variance+(c[i]-moyen)**2
    variance=variance/len(c)

    ecar_type=math.sqrt(variance)
    return ecar_type*len(itemset)

def minsup2(occurrence):
    occurrence = sorted(occurrence)
    s = int((occurrence[math.ceil(len(occurrence)/2)]-occurrence[0]) /2)
    return(s)


def aprpri(data,itemset,s):
  
    c = Counter()
    for i in itemset:
        for d in data:
            if(i in d):
                c[i]+=1
    l = Counter()
    for i in c:
        if(c[i] >= s):
            l[frozenset([i])]+=c[i]
    sl = l
    
    taille = 1
    for count in range (2,1000):
        nc = set()
        temp = list(l)
        for i in range(0,len(temp)):
            for j in range(i+1,len(temp)):
                t = temp[i].union(temp[j])
                if(len(t) == count):
                    nc.add(temp[i].union(temp[j]))
        nc = list(nc)
        c = Counter()
        for i in nc:
            c[i] = 0
            for q in data:
                temp = set(q)
                if(i.issubset(temp)):
                    c[i]+=1
        l = Counter()
        for i in c:
            if(c[i] >= s):
                l[i]+=c[i]
        if(len(l) == 0):
            break
        sl = l
        taille = count
    return sl

def close(data,itemset,occurrence,c,s):
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
        rules.append(close_regles(list(temp),close))

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
        
    return sl,rules 
    
def regle(data,sl):
    choosing=[]
    for l in sl:
        c = [frozenset(q) for q in combinations(l,len(l)-1)]
        mmax = 0
        for a in c:
            b = l-a
            ab = l
            sab = 0
            sa = 0
            sb = 0
            for q in data:
                temp = set(q)
                if(a.issubset(temp)):
                    sa+=1
                if(b.issubset(temp)):
                    sb+=1
                if(ab.issubset(temp)):
                    sab+=1
            temp = sab/sa*100
            if(temp > mmax):
                mmax = temp
            temp = sab/sb*100
            if(temp > mmax):
                mmax = temp
            choosing.append(((str(list(a))+" -> "+str(list(b))+" = "+str(sab/sa*100)+"%",sab/sa*100,sab/(sa*sb)),((str(list(b))+" -> "+str(list(a))+" = "+str(sab/sb*100)+"%"),sab/sb*100,sab/(sa*sb))))
        curr = 1
        for a in c:
            b = l-a
            ab = l
            sab = 0
            sa = 0
            sb = 0
            for q in data:
                temp = set(q)
                if(a.issubset(temp)):
                    sa+=1
                if(b.issubset(temp)):
                    sb+=1
                if(ab.issubset(temp)):
                    sab+=1
            temp = sab/sa*100
            curr += 1
            temp = sab/sb*100
            curr += 1
    return choosing

def fonction(x):
    max_choosing=[]
    for v in x:
        if v[0][1]>60:
            max_choosing.append(v[0])
        
        if v[1][1] >60:
            max_choosing.append(v[1])
    return max_choosing

def close_regles(itemset,close):
    regles=[]
    for i in itemset:
        if(len(close[i])>len(i)):
            close_list=list(close[i])
            rule=[]
            for k in close[i] :
                if(k not in i):
                    rule.append(k)
            regles.append(str(list(i))+"->"+str(rule))
    return regles


def find_key(v,dic_name): 
    for k, val in dic_name.items(): 
        if v == val: 
            return k 

def pretraitement1(data):
    n,m=data.shape
    nb_duplicate_value=[] 
    nb_missing_value=[]
    for j in range(m):
        nb_duplicate_value.append({})
        nb_missing_value.append(0)

    for j in range(m):
        for i in range(n):
            if (str(data[i][j]) in nb_duplicate_value[j]):
                nb_duplicate_value[j][str(data[i][j])]=nb_duplicate_value[j][str(data[i][j])]+1
            else:
                nb_duplicate_value[j][str(data[i][j])]=1
                
    for i in range(m):
        if 'none' in nb_duplicate_value[i]:
            nb_missing_value[i]=nb_duplicate_value[i]['none']
            del nb_duplicate_value[i]['none'] 

    les_val_les_plus_freq=[]
    for i in range(m):
        les_val_les_plus_freq.append(max(nb_duplicate_value[i].values()))

    for j in range(m):
        for i in range(n):
            if(str(data[i][j]) == 'none'):
                data[i][j] = str(find_key(les_val_les_plus_freq[j],nb_duplicate_value[j]))
                
    return data

def pretraitement2(data):
    n,m=data.shape
    value_column=[] 
    nb_missing_value=[]
    nb_iter=[]

    for j in range(m):
        value_column.append([])
        nb_missing_value.append(0)
        nb_iter.append(())

    for i in range(n):
        for j in range(m):
            if (data[i][j] not in value_column[j]):
                if(data[i][j]!="none"):
                    value_column[j].append(data[i][j])
                else:
                    nb_missing_value[j]=nb_missing_value[j]+1
    
    for j in range(m):
        if nb_missing_value[j] != 0:
            nb_iter[j]=nb_missing_value[j]//len(value_column[j])
        
    for j in range(m):
        iter=0
        index=0
        for i in range(n):
            if data[i][j]=="none" :
                if index<len(value_column[j]):
                    iter=iter+1
                    data[i][j]=value_column[j][index]
                
                    if (iter==nb_iter[j]):
                        iter=0
                        index=index+1
                else:
                    index=0
                    for k in range(i,n):
                        if data[i][j]=="none" :
                            data[i][j]=value_column[j][index]
                            index=index+1
                    i=n
    return data

def upper_matrice(data):
    for i in range(len(data)):
        for j in range(len(data[0])):
            data[i][j]=data[i][j].upper()
    return data
    