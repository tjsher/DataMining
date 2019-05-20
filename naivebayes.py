import pandas as pd
import collections as co
from functools import reduce



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


class NaiveBayesClassifer():
    def  __init__(self):
        pass

    def predict(self,data,test):
        self.fit(data,test)

    def fit(self,data,test):
        i = 0
        length = 14
        dataV = []
        pX = [] # p(X) , X = {x1,x2,x3....}
        pab = [[],[]] # p(a|b) 
        pba = [0,0] # p(b|a)
        pb = [0,0] #p(b)
        for feature in data: # count pX
            if(feature == 'play'):continue
            count = co.Counter()
            count.update(data[feature])
            pX.append(count[test[i]] / length)
            i += 1
        pX = reduce(lambda x,y:x * y,pX)
        dataV.append(data[data['play'].isin(['no'])])
        dataV.append(data[data['play'].isin(['yes'])])

        count = co.Counter() # count pb
        count.update(data['play'])
        pb[0] = count['no'] / length
        pb[1] = count['yes'] / length

        for d in dataV:#count pab
            i = 0
            for f in d:
                if(f == 'play'):continue
                count = co.Counter()
                count.update(d[f])
                if(set(list(d['play'])) == {'no'}):
                    pab[0].append(count[test[i]] / len(d))
                else:
                    pab[1].append(count[test[i]] / len(d))
                i += 1

        pab[0] = reduce(lambda x,y:x * y,pab[0])
        pab[1] = reduce(lambda x,y:x * y,pab[1])
        
        pba[0] = pab[0] * pb[0] / pX
        pba[1] = pab[1] * pb[1] / pX
 
        if(pba[0] >= pba[1]):
            print('result is no ---------',pba[0])

        if(pba[0] < pba[1]):
            print('result is yes --------',pba[1])
        

data = Read_files()
p = NaiveBayesClassifer()


test = ['sunny','hot','high','FALSE']
p.predict(data,test)
