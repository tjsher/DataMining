import numpy as np
import matplotlib.pyplot as plt
import math

def Read_files(FileName):
    file = open(FileName)
    lines= []
    labels = []
    res = []
    i = 0
    while True:
        line = file.readline().strip('\n')#remove '\n'
        if not line:
            break
        lines.append(line)
    temp = []
    for line in lines:#remove ','
        splited_data = line.split(',')
        temp.append(splited_data.pop())
        res.append(splited_data)

    for numbers in res:# str -> number
        for i in range(len(numbers)):
            numbers[i] = float(numbers[i])

    types = ['Iris-setosa','Iris-versicolor','Iris-virginica']
    for i in temp:# str -> number
        for j in range(len(types)):
            if(i == types[j]):
                labels.append(j)

    return res,labels

def Dist(p,q):# Distance
    return math.sqrt(np.power(p-q,2).sum())

def fit(data,k):
    distances = [[50000 for i in range(len(data))] for i in range(len(data))]
    sorted_d = [[] for i in range(len(data))]
    nok = [[] for i in range(len(data))] # neighbors of k-distance
    k_dist = []
    reach_dist = [[0 for i in range(len(data))] for i in range(len(data))]
    lrd = [] # local rechability density
    lof = [] # local outlier factor

    for p in range(len(data)):# caculate distance 
        for q in range(len(data)):
            if(q == p):continue
            d = Dist(np.array(data[p]),np.array(data[q]))
            distances[p][q] = d
        sorted_d[p] = sorted(distances[p])
        k_dist.append(sorted_d[p][k]) # k-distance

        #print("distances[%d]"%(p),sorted_d[p])
        #print("k_dist[%d]"%(p),k_dist[p])

        for q in range(len(data)):
            if(q == p):continue
            if(distances[p][q] <= k_dist[p]):
                nok[p].append([q,distances[p][q]])
        #print("nok[%d] ----- \n"%(p),nok[p])

    for p in range(len(data)):# caculate reach-distance 
        for q in range(len(data)):
            if(q == p):continue
            reach_dist[p][q] = max(k_dist[q],distances[p][q])
            #print("reach_dist[%d][%d]-------\n"%(p,q),reach_dist[p][q])

    for p in range(len(nok)):
        _sum = 0
        for i in range(k):
            _sum += reach_dist[p][nok[p][i][0]]
        _sum = k / _sum 
        lrd.append(_sum)

    for p in range(len(lrd)):
        _sum = 0
        for i in range(k):
            _sum += lrd[nok[p][i][0]]
        _sum = _sum / k
        _sum = _sum / lrd[p]
        lof.append(_sum)
    
    dic = {}
    for i in range(len(lof)):
        dic[lof[i]] = i
    lof = sorted(lof,reverse=True)
    for i in range(len(lof)):
        print(dic[lof[i]]+1,'-----',lof[i])

d,l = Read_files('iris.txt')# data is data set, labels are labels
k = 8
fit(d,k)