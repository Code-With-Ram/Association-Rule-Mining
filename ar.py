
#importing modules
import numpy as np
import pandas as pd
from itertools import combinations 
import matplotlib.pyplot as plt
minsup=minconf=N=minsupcount=FrequentItemsets=0

def importDataset(path):
    #importing dataset

    df = pd.read_csv(path)
    return df


def DataToMatrix(df):
    mat = {
            'id':[i for i in range(1,len(df)+1)]
    }
    
    l = set()
    for x in df.values:
        l=l.union(set(x[1:]))
    items = list(l)
    #print(items)
    for x in items:
        if str(x)=='nan':
            continue
        mat.update({x:[0 for i in range(1,len(df)+1)]})
    for i,x in enumerate(df.values):
        for y in x:
            if y in mat.keys():
                mat[y][i]=1

    df = pd.DataFrame(mat)
    df.to_csv('Market_Basket_Optimisation_Matrix.csv',index=False) 
    return df    

''' Functions related to Apriori and Generation of Frequent Itemsets''' 

def getSingleItemSets(a):
    res =[col for col in a.columns]
    return res


'''Caluculates suuport count for each item in the itemset
    a -> which subset
    data -> datamatrix
'''
def getSupCount(data,a):
    supcount=[0 for i in range(len(a))]
    for i,x in enumerate(a):
        if type(x)==type(list()):
            d = pd.DataFrame()
            for k in x:
                d[k]=data[k]
                
            for k in d.values:
                if sum(k)==len(x):
                    supcount[i]+=1
        else:
            supcount[i] = sum(data[x].values)
                
    
    return supcount

#Prunes the itemset which has supcount less than minsupcount
def pruning(itemset,minsupcount = 3):
    #print(itemset)
    a=[]
    for x in itemset:
        if x[1]>=minsupcount:
            a.append(x)
    
    itemset = a[:]
    return pd.DataFrame(itemset)


#Generates The l Itemset
def getItemSet(data,l):
    #print(data.values)
    t = set()
    for x in data.values:
        #print(x,'++>',type(x[0]))
        t=t.union(set(x[0])) if  type(x[0])==type(list()) else t.union(set(x))
    
    filt = list(t)
                    
    #print('x',l,filt)
    data =filt[:]
    comb = combinations(data,l)
    res =[]
    for x in np.array(list(comb)):
        #print(x,"\n\n")
        res.append([y for y in x])
    return (res)#np.array(list(comb))

def generateItemset(df,data,minsupcount,l=1):
    if l==1:
        a = getSingleItemSets(data)
    else:
        a = getItemSet(data,l)
    supcount = getSupCount(df,a)
    itemset= []
    for i in range(len(a)):
        itemset.append([a[i],supcount[i]])
    itemset =pruning(itemset,minsupcount)
    return itemset





#Generate Frequent Itemsets
def GetFrequentItemSets(df,minsupcount):
    FrequentItemsets=dict()
    l=generateItemset(df.iloc[:,1:],df.iloc[:,1:],minsupcount,1)
    FrequentItemsets.update({'l1':l})
    i=1
    while list(l)!=[]:
        l = generateItemset(df.iloc[:,1:],FrequentItemsets['l'+str(i)].iloc[:,:1],minsupcount,i+1)
        i+=1
        FrequentItemsets.update({'l'+str(i):l})
    return FrequentItemsets




#Finding Association Rules
def FindAssociationRules(df,itemset):
    #global l1,l2
    rules = {
            'antecedent':[],'consequent':[]
            }
    items=[x[0] for x in itemset.values]
    
    for x in items:
        for i in range(len(x)):
            rules['antecedent'].append(x[i])
            rules['consequent'].append(x[:i]+x[i+1:])
            rules['consequent'].append(x[i])
            rules['antecedent'].append(x[:i]+x[i+1:])

    rules = pd.DataFrame(rules)
    def getNumerator(data,x):

        for i in range(len(data)):
            x.sort()
            y = data[i][:1][0]
            y.sort()
            if x==y:
                return data[i][:][1]

    def getDenomenator(data,x,k) :
            if k==1:
                return sum(data[x].values)
            else:
                d = pd.DataFrame()
                for i in x:
                    d[i]=data[i]
                s = 0
                for i in d.values:
                    if sum(i)==len(x):
                        s+=1
                return s
    confidences = []
    for x in rules.values:
        if type(x[0]) == type(list()):
            s = x[0:1][0].copy()
            
            s.extend([x[1]])
        else:
            s = list(x[0:1]).copy()
            s.extend(x[1])
        
        n=getNumerator(itemset.values,s)
        d = getDenomenator(df,x[0],2) if type(x[0]) == type(list()) else getDenomenator(df,x[0:1],1)
        if type(d)==type(np.array([1])):
            d=d[0]
            
        confidences.append(n/d)
    rules['confidences'] =confidences


    #Support
    supports = []
    for x in rules.values:
        n=getNumerator(itemset.values,s)
        supports.append(n/N)
    rules['supports'] =supports

    #Lift
    lifts = []
    for i in range(len(supports)):
        #print(getSupCount(df,[rules.consequent[i]])[0]/N)
        l = confidences[i]/(getSupCount(df,[rules.consequent[i]])[0]/N)
        lifts.append(l)
    
    rules['lifts'] = lifts
    
    return rules
      










def FindStrongRules(rules,minconf):
    i =0
    while True:
        if i >= len(rules.values):
            break
        if rules.values[i][2] < minconf:
            rules.drop(rules.index[[i]],inplace=True)
            i-=1
        i+=1
    return rules






def plotItemsetSupcount(data):
    colors = ['red']
    names = ["Itemset"]
    x = data.iloc[:,:1].values
    y = data.iloc[:,1:].values
    xticks = [i[0] for i in x]
    xticks = list(np.array(xticks).T)
    fig, ax = plt.subplots()
    #print(list(np.array(xticks).T),y)
    
    pd.DataFrame(y, index=xticks, columns=names).plot.bar(color=colors, ax=ax)
    plt.show()



def Plot_Rules_Conf(rules):
    plt.style.use('ggplot')
    confidences = [ i/10 for i in range(2,8)]
    no_of_rules = [ len(FindStrongRules(rules.copy(),c)) for c in confidences] 
    plt.xlabel('Confidence Level')
    plt.yticks(range(len(rules)*2))
    plt.ylabel('No of Rules')
    plt.title('Apriori Algorithm at Different confidence')
    plt.plot(confidences,no_of_rules)
    plt.scatter(confidences,no_of_rules)
    plt.show()





def Plot_Rules_Conf_Sup(df):
    
    plt.title('Apriori Algorithm at Different confidence')
    plt.style.use('ggplot')
    plt.xlabel('Confidence Level')
    plt.ylabel('No of Rules')
    plt.yticks(range(0,60,6))
    
    colour=['red','blue','orange','black','cyan','gray']
    for i in range(2,5):
        minsupcount= (i/100.0)*len(df)
        FrequentItemsets = GetFrequentItemSets(df,minsupcount)
        rules = FindAssociationRules(df,FrequentItemsets[list(FrequentItemsets.keys())[-2]])

        confidences = [ i/10 for i in range(2,8)]
        no_of_rules = [ len(FindStrongRules(rules.copy(),c)) for c in confidences] 
        plt.plot(confidences,no_of_rules,color=colour[i-2],label='Support level '+str(i/100.0)+'%')
        plt.scatter(confidences,no_of_rules)
        plt.legend()
    
    plt.show()




def AssociationMain(path):
    global minsup, minconf, N, minsupcount, FrequentItemsets
    df = importDataset(path)
    minsup = 0.02
    minconf = 0.5
    N=len(df.values)
    minsupcount = int(minsup * N)
    FrequentItemsets = dict()
    df = DataToMatrix(df)
    FrequentItemsets = GetFrequentItemSets(df,minsupcount)
    print("Most frequent Itemset",FrequentItemsets['l'+str(len(FrequentItemsets)-1)])

    rules = FindAssociationRules(df,FrequentItemsets[list(FrequentItemsets.keys())[-2]])
    strongrules = FindStrongRules(rules.copy(),minconf)
    print('strongrules are ',strongrules)
    return df,rules,strongrules
    
    #Plot_Rules_Conf(rules)
    #Plot_Rules_Conf_Sup(df)

