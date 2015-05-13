__author__ = 'Milena'

import sys
from PyQt4 import QtGui
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import random
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import *

class kMeansGrouping(QtGui.QWidget):

    def __init__(self, dataFrame, _k, _metric):
        super(kMeansGrouping, self).__init__()

        self.df2 = dataFrame
        # df3.drop(labels=df3.columns[-1], axis=1)
        self.df = dataFrame.drop(labels=dataFrame.columns[-1], axis=1) #dane bez ostatniej kolumny-atrybutu decyzyjnego
        self.k = _k
        self.metric = _metric
        self.MAX_ITERATIONS = 100;

        self.kMeans()

    def kMeans(self):
        #first centroids found randomly from data points

        #centroids1 stores rows' indexes
        centroids1 = random.sample(self.df.index, self.k)
        d=[]
        for c in centroids1:
            d.append(self.df.loc[c])

        centroids = pd.DataFrame(data=d)
        centroids3 = centroids.values

        print "\ncentroids1: "
        print centroids1
        print "\n\n"
        print "\ncentroids: "
        print centroids
        print "\n\n"
        print "\ncentroids3: "
        print centroids3
        print "\n\n"

        # distance_array = np.sum((centroids.values - self.df.values)**2, axis=1)
        # print "\ndistance_array\n"
        # print distance_array

        odlCentroids=None
        iterations=0
        # while not self.stopCondition(flag, iterations):
        changed = True
        # while not changed or iterations < self.MAX_ITERATIONS:
            # odlCentroids=centroids
            # iterations+=1

        # centroids, changed = self.assignPoints(centroids)
        #labels are assigned centroids for each points, centroids are only k points
        labels, centroids = self.tmpAssignPoints(centroids3)

        centroids = self.recalculateCentroids(centroids,labels)
            # centroids = self.recalculateCentroids(c)

    def tmpAssignPoints(self, centroids):
        labels_centroids=[]
        for i in self.df.index:
            disctances=[]
            c_dist = []
            for c in centroids:
                # print "i: "+str(self.df.loc[i].values)+ " c: "+str(c)
                x= self.myEuclidean(self.df.loc[i].values, c)
                # print "xx: "+str(x)
                #klucz-x, wartosc-c
                disctances.append(x)
                c_dist.append(c)
            m = min(disctances)
            # print "distances:"
            # print  disctances
            # print "c_dist"
            # print c_dist
            dm = disctances.index(m)
            tmp_nearest_centr = c_dist[dm]
            labels_centroids.append(tmp_nearest_centr)
            # print"closest centr: "+str(tmp_nearest_centr )

        return (labels_centroids, centroids)





    def assignPoints(self, centroids):
        # centroids
        # l = len(centroids)
        # for i in range(0,l):
        #     centroids[i]+=random.random()

        #set to True when there is a change in assigning points to clusters(centroids)
        changed = False

        assignedCentroids = pd.DataFrame()
        for i in self.df.index:
            distances = {}
            for c in centroids.index:
                x = self.myEuclidean(self.df.loc[c], self.df.loc[i])
                # print"i: "+str(i)+" c: "+str(c)
                # print "self.df.loc[i]: "+ str(self.df.loc[i])
                # print "self.df.loc[c]: "+ str(self.df.loc[c])
                # print "x: "+str(x)
                #dictionary that stores centroid as a key and distance between point and centroid as a value
                distances[c] = x

            # find the minimum by comparing the second element of each tuple (values)
            m=min(distances.items(), key=lambda x: x[1])
            #m[0] is a key of a min value in a dictionary, so m[0] is centroid
            # point i 'belongs' to centroid m[0]
            # if not assignedCentroids.at[i,'centroids']==m[0]: #if centroid is changed
            #     changed=True
            # changed=True
            # assignedCentroids.at[i,'centroids']=m[0]
            assignedCentroids.at[i]=m[0]
        # print "centroidyyyyyyyyyy"
        # print assignedCentroids
        return (assignedCentroids, changed)

    def recalculateCentroids(self, centroids, labels):
        print "w recalculate, centroids: "
        print centroids
        print "\n"
        i=0
        #slownik, gdzie kazdemu centroidoi przypisana jest liczba identyfikujaca go
        tmp={}
        for c in centroids:
            i+=1
            tmp[tuple(c)]=i
        # print "\ntmp: "
        # print tmp

        tmpDf=self.df
        i=0
        for l in labels:
            tmpDf.ix[i,'labels']=tmp[tuple(l)]
            i+=1

        myMean = tmpDf.groupby('labels').mean()
        print "myMean"
        print myMean
        newCentroids=myMean.values
        # print "labels:"
        # print labels

        print "mymean values"
        print myMean.values
        print"\n\n"

        print "\n\ntmpDf"
        print tmpDf

        return newCentroids





    # algorithm terminates when there is no change in assigning points to clusters, none of the points chenged its cluster
    # so changed is False
    # or when the condition of max iterations is met
    def stopCondition(self, changed, iterations):
        if iterations > self.MAX_ITERATIONS:
            return True
        return not changed


    def myEuclidean(self,x,y):
        return np.sqrt(sum((x - y) ** 2))

    #wyswietla dialog do wpisania k i wywoluje okno do wybrania metryki
    def showDialogSelectK(self):
        kk, ok = QtGui.QInputDialog.getInt(self, "Wpisz k",
                "Wpisz liczbe klastrow k")

        if kk and ok:
            self.showDialogSelectMetric(kk)

    def showDialogSelectMetric(self, kk):
        item, ok = QtGui.QInputDialog.getItem(self, "Metryki",
                "Wybierz metryke", ('euklidesowa','inna nie dzialajaca'), 0, False)

        if item and ok:
            selectedMetric = item
            print "wybrana metryka " + selectedMetric