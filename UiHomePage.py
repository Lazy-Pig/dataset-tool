# coding: utf-8
from PyQt4 import QtCore, QtGui

class UiHomePage(QtGui.QWidget):
    def __init__(self, parent=None):
        super(UiHomePage, self).__init__()
        self.setupUi()
        self.show()
        self.raise_()

    def setupUi(self):
        self.showMaximized()
        self.totalWidget = QtGui.QGridLayout()
        self.setLayout(self.totalWidget)
        self.centralWidget = QtGui.QVBoxLayout()
        self.totalWidget.addLayout(self.centralWidget, 0, 0, 0, 2)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.centralWidget.addLayout(self.verticalLayout)
        self.startAndStopButton = QtGui.QPushButton("start")
        self.centralWidget.addWidget(self.startAndStopButton)

        self.displayResultLayout=QtGui.QGridLayout()
        self.totalWidget.addLayout(self.displayResultLayout, 0, 2, 0, 5)
        self.displayResultLayout.setSizeConstraint(QtGui.QLayout.SetMinAndMaxSize)
        self.tableDisplayResultTable=QtGui.QTableWidget()
        self.TableHBox_T = QtGui.QVBoxLayout()
        self.TableHBox_T.addWidget(self.tableDisplayResultTable)
        self.displayResultLayout.addLayout(self.TableHBox_T, 0, 0)
        header=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        self.tableDisplayResultTable.setColumnCount(10)
        self.tableDisplayResultTable.setHorizontalHeaderLabels(header)
        self.tableDisplayResultTable.setRowCount(50)



if __name__ == '__main__':
    app = QtGui.QApplication([])
    w = UiHomePage()
    app.exec_()