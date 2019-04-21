import numpy as np
import matplotlib.pyplot as plt
import random

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




class KMeans():
    def __init__(self, n_clusters=4):
        self.k = n_clusters

    def fit(self, data):
        """
        Fits the k-means model to the given dataset
        """
        n_samples, _ = data.shape
        # initialize cluster centers
        self.centers = np.array(random.sample(list(data), self.k))
        self.initial_centers = np.copy(self.centers)

        # We will keep track of whether the assignment of data points
        # to the clusters has changed. If it stops changing, we are 
        # done fitting the model
        old_assigns = None
        n_iters = 0

        while True:
            new_assigns = [self.classify(datapoint) for datapoint in data]

            if new_assigns == old_assigns:
                print(f"Training finished after {n_iters} iterations!")
                return

            old_assigns = new_assigns
            n_iters += 1

            # recalculate centers
            for id_ in range(self.k):
                points_idx = np.where(np.array(new_assigns) == id_)
                datapoints = data[points_idx]
                self.centers[id_] = datapoints.mean(axis=0)

    def l2_distance(self, datapoint):
        dists = np.sqrt(np.sum((self.centers - datapoint)**2, axis=1))
        return dists

    def classify(self, datapoint):
        """
        Given a datapoint, compute the cluster closest to the
        datapoint. Return the cluster ID of that cluster.
        """
        dists = self.l2_distance(datapoint)
        return np.argmin(dists)

    def plot_clusters(self, data):
        plt.figure(1)
        plt.title("Initial centers in black, final centers in red")
        k = 1
        for i in range(0,4):
            for j in range(0,4):
                plt.subplot(4,4,k)
                plt.scatter(data[:, i], data[:, j], marker='.', c=y)
                plt.scatter(self.centers[:, i], self.centers[:,j], c='r')
                plt.scatter(self.initial_centers[:, i], self.initial_centers[:,j], c='k')
                k += 1        
        plt.show() 

          
    

      
X,y = Read_files("iris.txt")
X = np.array(X)
kmeans = KMeans(n_clusters=3)
kmeans.fit(X)
kmeans.plot_clusters(X)
