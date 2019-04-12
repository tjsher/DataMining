
def Read_files(FileName):
    file = open(FileName)
    lines= []
    res = []
    i = 0
    while True:
        line = file.readline().strip('\n')#remove '\n'
        if not line:
            break
        lines.append(line)

    for line in lines:#remove ','
        splited_data = line.split(',')
        res.append(splited_data)

    return res

def Find_frequentOneSet(Data):
    tempSet = {}
    temp_deletes = []
    for data in Data:#caculate
    #data is ['a','b','c']
        for e in data:
            #e is 'a'
            if e not in tempSet:
                tempSet[e] = 1
            else:
                tempSet[e] += 1
    for key in tempSet:
        if(tempSet[key] < support):#remove if less than support
            temp_deletes.append(key)
    for temp_delete in temp_deletes:
        tempSet.pop(temp_delete)
    return tempSet

def Judge(l1,l2):#can connect or not
    flag = len(l1)
    if(l1[-1] == l2[-1]):#can't connect for the last item is not same
        return False

    for i in range(len(l1)):
        if(l1[i] == l2[i]):
            flag = flag - 1
    if(flag == 1):# can connect if k-1 set is same
        return True


def Get_candidate(tempSet):
    #tempSet is {'a':1,'b':2,'c':1}
    elems = []
    condidates = []
    for key1 in tempSet:
        #key1,key2 is the key of tempSet, such as 'a' or 'b' ...
        for key2 in tempSet:
            elems1 = key1.split(',')
            elems2 = key2.split(',')
            if(Judge(elems1,elems2)):# two k-1 set can connect
                elems1.append(elems2[-1])
                elems1.sort()
                tempString = ','.join(elems1)#connect
                if(tempString not in condidates):
                    condidates.append(tempString)
    return condidates

def Cut(condidates):
    Res = {}
    temp_deletes = []
    Data = Read_files(FileName)
    for data in Data:#count k-set
    #data is ['a','b','c']
        for C in condidates:
            count = 0
            length = 0
            for c in C.split(','):
                length += 1
                if(c in data):
                    count += 1
            if(count == length):
                if(C not in Res):
                    Res[C] = 1
                else:
                    Res[C] += 1

    print('--------before cutting---------\n',Res,'\n')
    for key in Res:
        if(Res[key] < support):
            temp_deletes.append(key)
    for temp_delete in temp_deletes:#remove if less than support
        Res.pop(temp_delete)

    for keys in Res:
        key = keys.split(',')

    print('--------after cutting---------\n',Res,'\n')

    return Res


def Get_rules(frequentSet):
    rules = []
    k = 1
    F = frequentSet[1:]#remove 1-Set
    #frequentSet[1:] store the information of 2,3,...k-set
    KFrequentSet = frequentSet[-1] #k-set
    #print("this is KFrequentSet\n",KFrequentSet)
    for current_FrequentSet in F:
        for keys in current_FrequentSet:
        #keys is the key of current frequentSet
            keyList = keys.split(',')#transform string to stringList
            #print("this is keyList",keyList)
            L = len(keyList)
            for i in range(1,L):
                KeyPermutations = Blend(keyList,i+1) #permutations of keys
                for items in KeyPermutations:
                    left = items.split('->')
                    total = []
                    #total = left[0]+','+left[1]
                    total.append(left[0])
                    total.append(left[1])
                    total.sort()
                    total = ','.join(total)
                    #rule is a,b->c,d
                    #a,b is left| c,d is right| total is a,b,c,d
                    tcount,rcount = 0,0

                    if total in frequentSet[Count_comma(total)]:
                            tcount += frequentSet[Count_comma(total)][total]
                    tcount = tcount / 14

                    right = left[-1].split(',')
                    right.sort()
                    right = ','.join(right)
                    if right in frequentSet[Count_comma(right)]:
                        rcount += frequentSet[Count_comma(right)][right]
                    rcount = rcount / 14

                    if(tcount / rcount > confidence):
                        a = sorted(left[0].split(','))
                        rules.append(right+'->'+','.join(a))
    return rules


def Count_comma(string):
    res = 0
    for i in string:
        if(i == ','):
            res += 1
    return res


def Blend(l,n): #list,number
    res = []
    if(len(l) < n): return False
    from itertools import combinations, permutations
    combs = list(permutations(l, n))  #combinations
    #combs is [(1,2,3),(2,1,3),(1,3,2)...]
    for comb in combs:  #transform tuple to string
        for i in range(1,n):
            temp1 = ','.join(comb[0:-i])
            length = len(comb[0:-i])
            temp2 = ','.join(comb[length:])
            res.append(temp1+'->'+temp2)

    return list(set(res))


support = 3
confidence = 0.6
FileName = "weather.nominal.txt"


def De_weighting(l):
    new_l = []
    for i in l:
        if i not in new_l:
            new_l.append(i)
    return new_l


if __name__=="__main__":
    Data = []
    tempSet = {}
    frequentSet = []
    Data = Read_files(FileName)#read files to obtain data
    tempSet = Find_frequentOneSet(Data)#find frequent 1-set
    while(tempSet):#not empty
        frequentSet.append(tempSet)
        condidates = Get_candidate(tempSet)
        #print('-----------condidates---------\n',condidates,'\n')
        tempSet = Cut(condidates)
    #for i in frequentSet:
        #print('-----------frequentSet---------\n',i,'\n')
    rules = Get_rules(frequentSet)
    rules = De_weighting(rules)
    rules.sort()
    for rule in rules:
        print('rule  :  ',rule)
