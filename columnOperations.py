__author__ = 'Milena'

import sys
from PyQt4 import QtGui
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import euclidean, cityblock, chebyshev, mahalanobis

class columnOperations(QtGui.QWidget):

    def __init__(self, dataFrame):
        super(columnOperations, self).__init__()

        self.df = dataFrame
        # self.initUI()

    def initUI(self):

        self.showDialogTextToNumber()

        # self.le = QtGui.QLineEdit(self)
        # self.le.move(130, 22)
        #
        # self.setGeometry(300, 300, 290, 150)
        # self.setWindowTitle('Input dialog')
        # self.show()

    def showDialogTextToNumber(self):
        item, ok = QtGui.QInputDialog.getItem(self, "Kolumny",
                "Wybierz kolumne", self.df.columns, 0, False)

        if item and ok:
            selectedColumn = item
            print "wybrana kolumna " + selectedColumn
            self.textToNumber(selectedColumn)

    #wybiera kolumne do dyskretyzacji i wywluje dialog box do wpisania liczby przedzialow
    def showDialogColumnRange(self):
        item, ok = QtGui.QInputDialog.getItem(self, "Kolumny",
                "Wybierz kolumne", self.df.columns, 0, False)

        if item and ok:
            selectedColumn = item
            print "wybrana kolumna " + selectedColumn
            self.showDialogRange(selectedColumn)

    #wyswietla dialog do wpisania liczby rzedzialow do dyskretyzacjii wywoluje fkcje disretize
    def showDialogRange(self, selectedColumn):
        range, ok = QtGui.QInputDialog.getInt(self, "Przedzialy",
                "Wpisz liczbe przedzialow")

        if range and ok:
            self.discretize(selectedColumn, range)

    def showDialogNormalize(self):
        item, ok = QtGui.QInputDialog.getItem(self, "Kolumny",
                "Wybierz kolumne", self.df.columns, 0, False)

        if item and ok:
            selectedColumn = item
            print "wybrana kolumna " + selectedColumn
            self.normalize(selectedColumn)

    def showDialogScatterPlotPlot(self):
        axisx, ok = QtGui.QInputDialog.getItem(self, "Os X",
                "Wybierz kolumne dla osi x", self.df.columns, 0, False)

        if axisx and ok:
            axisy, ok2 = QtGui.QInputDialog.getItem(self, "Os Y",
                "Wybierz kolumne dla osi y", self.df.columns, 0, False)
            if axisy and ok2:
                decClass, ok = QtGui.QInputDialog.getItem(self, "Klasa decyzyjna",
                        "Wybierz klase decyzyjna", self.df.columns, 0, False)
                if decClass and ok:
                    pd.options.display.mpl_style = 'default'
                    ttn = self.textToNumber(decClass)
                    self.df.plot(kind='scatter', x=str(axisx), y=str(axisy), c=ttn, s=40);

    def discretize(self, selectedColumn, range):
        l = []
        count = 0
        while (count <= range-1):
            l.append(count)
            count += 1

        if range == 0:
            l.append(0)

        try:
            discretized = pd.cut(self.df[str(selectedColumn)], range, labels=l)
            self.df['dyskr. przedz: '+ str(range)+' kol: '+str(selectedColumn)] = discretized
            print "zdyskretyzowana kolumna"
            print(discretized.values)
        except:
            pass

    def normalize(self, selectedColumn):
        mean = self.df[str(selectedColumn)].mean()
        standardDeviation = self.df[str(selectedColumn)].std()
        print "srednia: " + str(mean)
        print "odch stand: " + str(standardDeviation)
        try:
            self.df["znormaliz. "+str(selectedColumn)] = \
                (self.df[str(selectedColumn)] - mean) / standardDeviation
        except:
            pass

    def textToNumber(self, selectedColumn):
        tmp = {}
        list = []
        heading = str(selectedColumn)
        # print self.df['Hrabstwo']
        j = 0
        for i in self.df[heading]:
            try:
                tmp[i]
                list.append(tmp[i])
            except:
                j = j + 1
                tmp.update({i : j})
                list.append(j)

        self.df['num. ' + heading] = list
        return list

    def knn(self, metric):
        print "knn"
        print metric
        dfTmp = self.df
        # attributes = dfTmp.index[:-1] #do n-1
        attributes = self.df.index[:-1]
        dfDistances = pd.DataFrame(index=attributes, columns=attributes) #DataFrame do przechowywania odleglosci
        distCount = None                                                    #miedzy wszystkimi obiektami
        if metric == 'manhattan':
            distCount = lambda x, y: cityblock(x, y)
        elif metric == 'infinity':
            distCount = lambda x, y: chebyshev(x, y)
        elif metric == 'mahalanobis':
            try:
                cov = np.linalg.inv(dfTmp.ix[:, :-1].cov().as_matrix()) #macierz kowariancji
                distCount = lambda x, y: mahalanobis(x, y, cov)
            except:
                return
        else:
            distCount = lambda x, y: euclidean(x, y)

        #uzupelnienie macierzy odleglosci
        for i in attributes:
            for j in attributes:
                if i == j:
                    dfDistances.ix[i, j] = np.inf
                elif not np.isnan(dfDistances.ix[j, i]):
                    dfDistances.ix[i, j] = dfDistances.ix[j, i]
                else:
                    dfDistances.ix[i, j] = distCount(dfTmp.ix[i, :-1], dfTmp.ix[j, :-1])

        # print dfDistances

        # print("\n narest neighbours :")

        decisionAttributes = dfTmp.ix[:, -1] #atrybut decyzyjny - ostatnia kolumna
        # print "decision attr"
        # print(decisionAttributes)

        x=0
        result = pd.Series(0, index=range(1, len(attributes)))
        for i in attributes:
            sortedDist = dfDistances.ix[:,i].order()
            for j in range(1, len(attributes)):
                nNearestNeighbours = sortedDist.head(j).reset_index().ix[:, 0] #--head(n) return first n rows
                mostpopular = nNearestNeighbours.apply(lambda z: decisionAttributes[z]).value_counts().idxmax() #find the most frequent value in a column,
                if mostpopular == decisionAttributes[i]:											#choose the earlier element when breaking ties
                    # print "mostpopular: "
                    # print mostpopular
                    # print "decAttr: "
                    # print decisionAttributes[i]
                    result[j] += 1
                x+=1
                # print "RESULT: "
                # print result

                # print "j: "+ str(j)
                # maxCountDecAttr = nNearestNeighbours. #najliczniejsza klasa decyzyjny wsrod najblizszych sasiadow
                # print nNearestNeighbours

            # print "najblizsi sasiedzi: "
            # print nNearestNeighbours
        count = len(attributes)
        print count
        r2 = (result/count)*100
        # result = result.apply(lambda x: (x / count ) * 100)
        pd.options.display.mpl_style = 'default'
        r2.plot()
        print "RESULT22222222222222222222222: "
        print result
        # print len(attributes)
        # print attributes
        print "prtla wykonala sie: "
        print x

    def getDataFrame(self):
        return self.df


