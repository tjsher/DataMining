import math
import numpy as np
import matplotlib.pyplot as plt

class DBSCAN():

    def __init__(self):
        self.r = 0.15# radius
        self.MinPts = 8
        self.FileName = "iris.txt"
        self.visited = [0 for i in range(150)]# initially, all points are unvisitedPointvisited
        self.cluster = {}
        self.cp = []


    def Read_files(self):
        file = open(self.FileName)
        lines= []
        labels = []
        res = []
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


    def Dist(self,p,q):# Distance
        #return math.sqrt(np.power(p-q,2).sum())
        return np.power(p-q,2).sum()


    def All_are_visited(self):
        if(self.cp == []):
            return True
        else:
            return False


    def Get_random_start(self):# a random point from core points
        import random
        i = random.randint(0,len(self.cp) - 1)
        return self.cp[i]
        
    
    def fit(self):
        d,labels = self.Read_files()# d is data set, labels are labels
        a = []
        pon = [[] for i in range(len(d))]# point of neighbors
        for p in range(len(d)):
            _dist = []
            for q in range(len(d)):
                if(q == p):continue
                if(self.Dist(np.array(d[p]),np.array(d[q])) - self.r <= 1e-8):
                    pon[p].append(q)

        for p in range(len(pon)):
            if(len(pon[p]) >= 8):# is a core point
                self.cp.append(p)
            else:
                a.append(p)
        print('--------a----------',a)


        queue = []    
        while(not self.All_are_visited()):
            p = self.Get_random_start()
            if(self.visited[p] == 0):# not visited
                self.cluster[p] = [p]# create a new cluster named p
                self.visited[p] = 1
                queue.append(p)

                while(len(queue) > 0):# find another core point in neighbors of point p
                    q = queue.pop(0)
                    if(self.visited[q] == 0):
                        self.cluster[p].append(q)
                        self.visited[q] = 1

                    if(q in self.cp):# neighbor q is a core point
                        self.cp.pop(self.cp.index(q))
                        for i in pon[q]:
                            if(self.visited[i] == 0):
                                queue.append(i)
                                self.visited[i] = 1
                                self.cluster[p].append(i)
        for i in self.cluster:
            print('-------len---------',len(self.cluster[i]))
            print('------cluster%d------'%(i),self.cluster[i],'\n\n')

    def draw(self):
        data,labels = self.Read_files()
        c = []
        d = list(data)
        for i in self.cluster:
            temp = []
            for j in self.cluster[i]:
                temp.append(data[j])
                d.remove(data[j])
            c.append(temp)
        for i in range(len(c)):
            c[i] = np.array(c[i])
        d = np.array(d)
        data = np.array(data)
        plt.figure(1)
        plt.title("Initial centers in black, final centers in red")
        k = 1
        for i in range(0,4):
            for j in range(0,4):
                plt.subplot(4,4,k)
                plt.scatter(d[:, i], d[:, j],s=2, c='#000000')
                plt.scatter(c[0][:,i], c[0][:,j],s=0.8, c='r')
                plt.scatter(c[1][:,i], c[1][:,j],s=0.8, c='y')
                plt.scatter(c[2][:,i], c[2][:,j],s=0.8, c='b')
                k += 1        
        plt.show() 


a = DBSCAN()
a.fit()
a.draw()