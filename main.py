__author__ = 'Milena'

import sys
from window import *
import pandas as pd
from pandas import DataFrame, read_csv
from pandas.sandbox.qtpandas import DataFrameModel, DataFrameWidget
from PyQt4 import QtCore, QtGui


def main():
    """Main entry point for the script."""

    app = QtGui.QApplication(sys.argv)
    ex = MyWindow()
    sys.exit(app.exec_())
    #wczytanie danych baz nazw kolumn w pliku
    # pd.read_csv('INCOME.txt', comment='#', header=None, sep='\t')

    # df.describe()
    # datatable = QtGui.QTableWidget()
    # datatable.setColumnCount(len(df.columns))
    # datatable.setRowCount(len(df.index))
    # for i in range(len(df.index)):
    #     for j in range(len(df.columns)):
    #         datatable.setItem(i,j,QtGui.QTableWidgetItem(str(df.iget_value(i, j))))

# class MainWidget(QtGui.QWidget):
#     def __init__(self, parent=None):
#         super(MainWidget, self).__init__(parent)
#
#         # Create two DataFrames
#         self.df1 = pd.DataFrame(np.arange(9).reshape(3, 3),
#                                 columns=['foo', 'bar', 'baz'])
#         self.df2 = pd.DataFrame({
#                 'int': [1, 2, 3],
#                 'float': [1.5, 2.5, 3.5],
#                 'string': ['a', 'b', 'c'],
#                 'nan': [np.nan, np.nan, np.nan]
#             }, index=['AAA', 'BBB', 'CCC'],
#             columns=['int', 'float', 'string', 'nan'])
#
#         # Create the widget and set the first DataFrame
#         self.widget = DataFrameWidget(self.df1)
#
#         # Create the buttons for changing DataFrames
#         self.button_first = QtGui.QPushButton('First')
#         self.button_first.clicked.connect(self.on_first_click)
#         self.button_second = QtGui.QPushButton('Second')
#         self.button_second.clicked.connect(self.on_second_click)
#
#         # Set the layout
#         vbox = QtGui.QVBoxLayout()
#         vbox.addWidget(self.widget)
#         hbox = QtGui.QHBoxLayout()
#         hbox.addWidget(self.button_first)
#         hbox.addWidget(self.button_second)
#         vbox.addLayout(hbox)
#         self.setLayout(vbox)
#
#     def on_first_click(self):
#         '''Sets the first DataFrame'''
#         self.widget.setDataFrame(self.df1)
#
#     def on_second_click(self):
#         '''Sets the second DataFrame'''
#         self.widget.setDataFrame(self.df2)

if __name__ == '__main__':
    main()

    # Initialize the application
    # app = QtGui.QApplication(sys.argv)
    # mw = MainWidget()
    # mw.show()
    # app.exec_()