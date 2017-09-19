# coding: utf-8
from PyQt4 import QtCore, QtGui

class UiHomePage(QtGui.QWidget):
    def __init__(self, parent=None):
        super(UiHomePage, self).__init__()
        self.setupUi()
        self.show()
        self.raise_()

    def setupUi(self):
        # 设置窗口大小为最小
        self.showMinimized()
        self.centralWidget = QtGui.QVBoxLayout()

        # 设置全局的layout
        self.setLayout(self.centralWidget)

        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.centralWidget.addLayout(self.verticalLayout_2)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.lineEdit_IPFile = QtGui.QLineEdit()
        self.centralWidget.addWidget(self.lineEdit_IPFile)
        self.horizontalLayout_6.addWidget(self.lineEdit_IPFile)
        self.Button_Open = QtGui.QPushButton("Open")
        self.centralWidget.addWidget(self.Button_Open)
        self.horizontalLayout_6.addWidget(self.Button_Open)
        self.verticalLayout_2.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_4 = QtGui.QHBoxLayout()

        self.listView = QtGui.QListView()
        self.centralWidget.addWidget(self.listView)
        self.horizontalLayout_4.addWidget(self.listView)
        self.listView.setSpacing(4)
        # self.listView.clicked.connect(self.on_listView_cliked)

        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()

        # add the progressbar
        self.progressBar = QtGui.QProgressBar()
        self.centralWidget.addWidget(self.progressBar)
        self.progressBar.setProperty("value", 0)
        style = """
                QProgressBar {
                    border: 2px solid grey;
                    border-radius: 5px;
                    text-align: center;
                }

                QProgressBar::chunk {
                    background-color: #88B0EB;
                    width: 20px;
                }"""
        self.progressBar.setStyleSheet(style)
        ###############################################################

        self.Button_Plus = QtGui.QPushButton("+")
        # self.Button_Plus.clicked.connect(self.Click_Plus)
        self.Button_Minus = QtGui.QPushButton("-")
        # self.Button_Minus.clicked.connect(self.Clik_Minus)
        self.PMHbox = QtGui.QHBoxLayout()
        self.PMHbox.addWidget(self.Button_Plus)
        self.PMHbox.addWidget(self.Button_Minus)
        self.PMHbox.addStretch(1)

        self.PMVbox = QtGui.QVBoxLayout()
        self.PMVbox.addLayout(self.PMHbox)
        self.horizontalLayout_3.addWidget(self.progressBar)

        self.verticalLayout_2.addLayout(self.PMVbox)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.horizontalLayout = QtGui.QHBoxLayout()

        self.Button_Cancel = QtGui.QPushButton("Start")
        self.centralWidget.addWidget(self.Button_Cancel)
        self.horizontalLayout.addWidget(self.Button_Cancel)

        self.Button_Display = QtGui.QPushButton("Cancel")
        self.centralWidget.addWidget(self.Button_Display)
        self.horizontalLayout.addWidget(self.Button_Display)
        # self.Button_Display.clicked.connect(self.Display)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2.addLayout(self.verticalLayout)

if __name__ == '__main__':
    app = QtGui.QApplication([])
    w = UiHomePage()
    app.exec_()