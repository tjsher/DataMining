import math
import collections as con
import pandas as pd
from sklearn import tree
from sklearn.datasets import load_iris
import graphviz
def Read_files():
    file = open("weather.nominal.txt")
    lines = []
    res = []
    while True:
        line = file.readline().strip('\n')  # remove '\n'
        if not line:
            break
        lines.append(line)
        temp = []
    for line in lines:  # remove ','
        splited_data = line.split(',')
        #labels.append(splited_data.pop())
        res.append(splited_data)
    p = pd.DataFrame(data=res, columns=['outlook','temperature',
                        'humidity','windy','play'])
        
    return p

def Is_SameType(data):
    res = con.Counter()
    res.update(data)
    return len(res) == 1

def Split_Data(data,feature):
    res = {}
    d = set(list(data[feature]))
    for v in d:
        tmp = data[data[feature] == v]
        tmp.drop([feature],axis = 1,inplace=True)
        res[v] = tmp
    return res

def Count_Labels(data):
    res = con.Counter()
    res.update(data['play'])
    _max = 0
    if(res['yes'] > res['no']):return 'yes'
    else:   return 'no' 


class DTreeNode():

    def __init__(self,data,features = ['outlook','temperature',
                        'humidity','windy','play']):
        self.data = data
        self.features = features
        self.children = {}
        self.values = 0

    def Entropy(self,data):
        #E(X)
        res = con.Counter()
        res.update(data)
        ent = 0
        length = len(data)

        for r in res.values():
            if(r == 0):
                continue 
            p = float(r) / length
            ent -= p * math.log2(p)

        return ent
        
    def Condition_Entropy(self,data,feature):
        # E(Y|x)
        d = list(data[feature])
        labels = list(data['play'])
        dic = {}
        for i in range(len(d)):
            if(d[i] not in dic):
                dic[d[i]] = [0,0] # yes,no
            if(labels[i] == 'yes'):
                dic[d[i]][0] += 1
            elif(labels[i] == 'no'):
                dic[d[i]][1] += 1        

        temp = 0
        res = 0
        for key in dic:

            n = dic[key][0] + dic[key][1]
            temp = ['yes']*dic[key][0] +['no']*dic[key][1]
            temp = self.Entropy(temp)
            res += temp * n / 14
        return res

    def Infomation_Gain(self,data,f):
        bEnt = self.Entropy(data)
        aEnt = self.Condition_Entropy(data, f)
        return bEnt - aEnt

    def Best_Feature(self):
        _max,bestFeature =0,0
        for f in self.features:
            if(f == 'play'):    break
            ig = self.Infomation_Gain(self.data, f)
            if(ig > _max):
                _max = ig
                bestFeature = f
        return bestFeature

class DTree():

    def __init__(self):
        self.root = None
        self.queue = []
        self.length = [1]


    def Print(self,node,n):
        if(node.values == 'yes' or node.values == 'no'):
            print('|------'*n,'%s'%(node.values))
        else:
            print('|------'*n,'%s = ?'%(node.values))
        for key in node.children:
            print('|------'*n,'%s = %s'%(node.values,key))
            self.Print(node.children[key],n+1)


    def Tree_Generate(self,data,features):

        node = DTreeNode(data,features)

        if(Is_SameType(data['play'])): # is leaf
            node.values = Count_Labels(data)
            return node

        bestFeature = node.Best_Feature()
        if(node.Infomation_Gain(data,bestFeature) <= 0.1):# threshold
            node.values.append(Count_Labels(data))
            return node

        node.values = bestFeature
        dic = Split_Data(data, bestFeature)
        features.remove(bestFeature)

        for key in dic:
            node.children[key] = self.Tree_Generate(dic[key], features)

        return node


    def fit(self,data,features):
        self.root = self.Tree_Generate(data, features)
        self.Print(self.root,0)

    def predict(self,sample):
        p = pd.DataFrame(data=sample, columns=['outlook','temperature',
                        'humidity','windy'])
        res = self.root
        while(True):
            res = res.children[p[res.values]]
            if(res.values == 'yes' or res.values == 'no'):break
        print(res.values)

root = DTree()
root.fit(Read_files(),['outlook','temperature',
                       'humidity','windy','play'])

#root.predict(['sunny','hot','high','FALSE'])
