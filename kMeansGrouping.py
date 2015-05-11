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

        self.kMeans()

    def kMeans(self):
        #first centroids found randomly from data
        print "k: "
        print self.k
        centroids = random.sample(self.df.index, self.k)
        print "\ncentroids: "
        print centroids
        print "\n\n"

        # centroids
        # l = len(centroids)
        # for i in range(0,l):
        #     centroids[i]+=random.random()

        # x=df3.loc[3]
        # b= x.count()
        # for i in range(0, b):
        #     f=random.random()
        #     print f
        #     x[i]+=f

        for c in centroids:
            distances = []
            # print "\nitemC: "
            # print self.df.loc[c]
            for i in self.df.index:
                # print "\nitemi: "
                # print self.df.loc[i]
                x = self.myEuclidean(self.df.loc[c], self.df.loc[i])
                # print "c: "
                # print c
                distances.append(x)


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