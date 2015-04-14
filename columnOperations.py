__author__ = 'Milena'

import sys
from PyQt4 import QtGui
import pandas as pd
import matplotlib.pyplot as plt

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
                print "teraz wysuje wykres"
                pd.options.display.mpl_style = 'default'
                self.df.plot(kind='scatter', x=str(axisx), y=str(axisy), c=self.textToNumber('Hrabstwo'), s=100);

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

    def getDataFrame(self):
        return self.df


