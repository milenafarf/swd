__author__ = 'Milena'

import sys
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import *
import pandas as pd
from pandas.sandbox.qtpandas import DataFrameModel, DataFrameWidget
from columnOperations import *
from kMeansGrouping import *

class MyWindow(QtGui.QMainWindow):

    def __init__(self):
        super(MyWindow, self).__init__()

        self.initUI()

    def initUI(self):
        self.df = None
        self.colOp = None
        self.kMeans = None

        # T E M P O R A R Y READ FROM FILE
        self.df =  pd.read_csv("INCOME.csv", comment='#', header=0, sep='\t')
        self.widget = DataFrameWidget(self.df)
        self.setCentralWidget(self.widget)
        self.colOp = columnOperations(self.df)
        # T E M P O R A R Y READ FROM FILE

        openFile = QtGui.QAction(QtGui.QIcon('open.png'), 'Wczytaj dane', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.showDialogFile)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&Plik')
        fileMenu.addAction(openFile)

        textToNumber = QtGui.QAction('Zamien dane tekstowe na numeryczne', self)
        textToNumber.setShortcut('Ctrl+T')
        textToNumber.triggered.connect(self.showDialogTextToNumber)

        discretize = QtGui.QAction('Dyskretyzacja', self)
        discretize.setShortcut('Ctrl+D')
        discretize.triggered.connect(self.showDialogDiscretize)

        normalize = QtGui.QAction('Normalizacja', self)
        normalize.setShortcut('Ctrl+N')
        normalize.triggered.connect(self.showDialogNormalize)

        columnMenu = menubar.addMenu('&Kolumny')
        columnMenu.addAction(textToNumber)
        columnMenu.addAction(discretize)
        columnMenu.addAction(normalize)

        scatterPlot = QtGui.QAction('Wykres rozproszen dwuwymiarowy', self)
        scatterPlot.setShortcut('Ctrl+R')
        scatterPlot.triggered.connect(self.showDialogScatterPlotPlot)

        plotMenu = menubar.addMenu('&Wykres')
        plotMenu.addAction(scatterPlot)

        euclid = QtGui.QAction('odleglosc Euklidesowa', self)
        euclid.setShortcut('Ctrl+E')
        euclid.triggered.connect(self.showDialogKnnEuclidean)
        manhattan = QtGui.QAction('metryka Manhattan', self)
        manhattan.setShortcut('Ctrl+M')
        manhattan.triggered.connect(self.showDialogKnnManhattan)
        nieskonczonosc = QtGui.QAction('nieskonczonosc', self)
        nieskonczonosc.triggered.connect(self.showDialogKnnInfinity)
        mahalanobis = QtGui.QAction('Mahalanobisa', self)
        mahalanobis.triggered.connect(self.showDialogKnnMahalanobis)

        knnMenu = menubar.addMenu('&Klasyfikacja metoda k-nn')
        knnMenu.addAction(euclid)
        knnMenu.addAction(manhattan)
        knnMenu.addAction(nieskonczonosc)
        knnMenu.addAction(mahalanobis)

        knn = QtGui.QAction('Grupowanie', self)
        knn.triggered.connect(self.showDialogKMeansGrouping)

        knnMenu = menubar.addMenu('&Grupowanie k-nn')
        knnMenu.addAction(knn)



        #
        # btn = QtGui.QPushButton('wczytaj dane', self)
        # btn.move(0, 30)

        self.setGeometry(300, 300, 500, 400)
        self.setWindowTitle('swd')
        self.show()

    def showDialogHeadline(self):
        # https://github.com/Werkov/PyQt4/blob/master/examples/dialogs/standarddialogs.py
        radio2 = QRadioButton("&nie")
        items = ("tak", "nie")
        item, ok = QtGui.QInputDialog.getItem(self, "Naglowki",
                "Czy wczytac z naglowkami?:", items, 0, False)

        if item and ok:
            if item == "tak":
                print item
                self.h = 0
            else:
                self.h = None
        #
        # checkbox, ok = QtGui.QInputDialog.getText(self, 'Input Dialog',
        #     'Enter your name:')

        if ok:
            self.showDialogFile()

    def showDialogFile(self):
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file', '/home',
                                                  'CSV files (*.csv);;Text files (*.txt)')
        f = open(fname, 'r')
        with f:
            self.df = pd.read_csv(f, comment='#', header = 0, sep='\t')
            self.colOp = columnOperations(self.df)
        # print df[0:10]
        self.widget = DataFrameWidget(self.df)
        self.setCentralWidget(self.widget)


    def showDialogTextToNumber(self):
        if self.colOp is not None:
            self.colOp.showDialogTextToNumber()
            self.df = self.colOp.getDataFrame()
            self.widget.setDataFrame(self.df)
        else:
            self.showAlertReadData()

    def showDialogDiscretize(self):
        if self.colOp is not None:
            self.colOp.showDialogColumnRange()
            self.df = self.colOp.getDataFrame()
            self.widget.setDataFrame(self.df)
        else:
            self.showAlertReadData()

    def showDialogNormalize(self):
        if self.colOp is not None:
            self.colOp.showDialogNormalize()
            self.df = self.colOp.getDataFrame()
            self.widget.setDataFrame(self.df)
        else:
            self.showAlertReadData()

    def showDialogScatterPlotPlot(self):
        if self.colOp is not None:
            self.colOp.showDialogScatterPlotPlot()
        else:
            self.showAlertReadData()

    def showDialogKnnEuclidean(self):
        if self.colOp is not None:
            self.colOp.knn('euclidean')
        else:
            self.showAlertReadData()

    def showDialogKnnManhattan(self):
        if self.colOp is not None:
            self.colOp.knn('manhattan')
        else:
            self.showAlertReadData()

    def showDialogKnnInfinity(self):
        if self.colOp is not None:
            self.colOp.knn('infinity')
        else:
            self.showAlertReadData()

    def showDialogKnnMahalanobis(self):
        if self.colOp is not None:
            self.colOp.knn('mahalanobis')
        else:
            self.showAlertReadData()

    def showDialogKMeansGrouping(self):
        if self.df is not None:
            self.showDialogSelectK()
        else:
            self.showAlertReadData()

    def showDialogSelectK(self):
        kk, ok = QtGui.QInputDialog.getInt(self, "Wpisz k",
                "Wpisz liczbe klastrow k")

        if kk and ok:
            if kk > 0:
                self.showDialogSelectMetric(kk)

    def showDialogSelectMetric(self, kk):
        item, ok = QtGui.QInputDialog.getItem(self, "Metryki",
                "Wybierz metryke", ('euklidesowa','inna nie dzialajaca'), 0, False)

        if item and ok:
            selectedMetric = item
            print "wybrana metryka " + selectedMetric
            self.kMeans = kMeansGrouping(self.df, kk, selectedMetric)


    def showAlertReadData(self):
        msgBox = QMessageBox()
        msgBox.setWindowTitle("Uwaga!")
        msgBox.setText("Najpierw musisz wczytac dane \n(skrot Ctrl+O)")
        msgBox.exec_()

