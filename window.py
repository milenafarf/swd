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
        self.metric = "euclidean"

        # T E M P O R A R Y READ FROM FILE
        # self.df =  pd.read_csv("INCOME.csv", comment='#', header=0, sep='\t')
        # self.widget = DataFrameWidget(self.df)
        # self.setCentralWidget(self.widget)
        # self.colOp = columnOperations(self.df)
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

        groupingEuclidean = QtGui.QAction('Grupowanie metryka euklides', self)
        groupingEuclidean.triggered.connect(self.showDialogKMeansGroupingEuclidean)
        groupingChebyshev = QtGui.QAction('Grupowanie metryka Chebyshev (nieskonczonosc)', self)
        groupingChebyshev.triggered.connect(self.showDialogKMeansGroupingChebyshev)
        groupingCityblock = QtGui.QAction('Grupowanie metryka Cityblock (l1)', self)
        groupingCityblock.triggered.connect(self.showDialogKMeansGroupingCityblock)
        groupingJacc = QtGui.QAction('Wspolczynnik Jaccarda', self)
        groupingJacc.triggered.connect(self.showDialogJaccardIndex)

        # showDialogKMeansGroupingEuclidean
        # showDialogKMeansGroupingChebyshev
        # showDialogKMeansGroupingCityblock

        groupingMenu = menubar.addMenu('&Grupowanie')
        groupingMenu.addAction(groupingEuclidean)
        groupingMenu.addAction(groupingChebyshev)
        groupingMenu.addAction(groupingCityblock)
        groupingMenu.addAction(groupingJacc)



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
            self.attributesNum = len(self.df.columns)-1
            self.colOp = columnOperations(self.df, self.attributesNum)
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

    def showDialogKMeansGroupingEuclidean(self):
        self.metric = "euclidean"
        if self.df is not None:
            self.showDialogSelectK()
        else:
            self.showAlertReadData()

    # chebyshev = nieskonczonosc
    def showDialogKMeansGroupingChebyshev(self):
        self.metric = "chebyshev"
        if self.df is not None:
            self.showDialogSelectK()
        else:
            self.showAlertReadData()

    # cityblock = l1
    def showDialogKMeansGroupingCityblock(self):
        self.metric = "cityblock"
        if self.df is not None:
            self.showDialogSelectK()
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
                self.showDialogSelectMaxIter(kk)

    def showDialogSelectMaxIter(self, kk):
        item, ok = QtGui.QInputDialog.getInt(self, "Max iteracji",
                "Mozesz podac, ile iteracji algorytm ma sie wykonywac\n Algorytm zakonczy sie wczesniej,jesli centroidy nie beda sie zmieniac")

        if item and ok:
            maxIter = item
            print "wybrana max iteracji " + str(maxIter)
            self.kMeans = kMeansGrouping(self.df, kk, self.metric, self.attributesNum, maxIter)
            self.df = self.kMeans.getDataFrame()
            self.widget.setDataFrame(self.df)
            # self.df['clusters']=self.kMeans.getLabelsNumeric()

    def showDialogJaccardIndex(self):
        self.kMeans.showDialogJaccardIndex1(self.df)


    def showAlertReadData(self):
        msgBox = QMessageBox()
        msgBox.setWindowTitle("Uwaga!")
        msgBox.setText("Najpierw musisz wczytac dane \n(skrot Ctrl+O)")
        msgBox.exec_()

