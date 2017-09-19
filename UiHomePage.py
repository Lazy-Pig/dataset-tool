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
        self.displayResultLayout = QtGui.QGridLayout()
        self.totalWidget.addLayout(self.displayResultLayout, 0, 2, 0, 5)
        self.displayResultLayout.setSizeConstraint(QtGui.QLayout.SetMinAndMaxSize)
        self.TableHBox_B = QtGui.QHBoxLayout()
        self.UpdateTable_Button = QtGui.QPushButton("Update")
        self.ExportTable_Button = QtGui.QPushButton("Export")
        self.TableHBox_B.addStretch(1)
        self.TableHBox_B.addWidget(self.UpdateTable_Button)
        self.TableHBox_B.addWidget(self.ExportTable_Button)
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
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.label = QtGui.QLabel("    Input the IP:")
        self.centralWidget.addWidget(self.label)
        self.horizontalLayout_5.addWidget(self.label)

        # combobox ui
        self.comboBox = QtGui.QComboBox()
        self.centralWidget.addWidget(self.comboBox)

        self.comboBox.setEditable(True)
        self.comboBox.setInsertPolicy(QtGui.QComboBox.InsertAtBottom)
        self.comboBox.setObjectName("comboBox")
        self.horizontalLayout_5.addWidget(self.comboBox)

        self.Button_ScanIP = QtGui.QPushButton("Scan IP")
        self.centralWidget.addWidget(self.Button_ScanIP)
        self.horizontalLayout_5.addWidget(self.Button_ScanIP)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
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
        self.Button_OpenPath = QtGui.QPushButton("Open Path")
        self.centralWidget.addWidget(self.Button_OpenPath)
        self.PMHbox.addWidget(self.Button_OpenPath)
        self.PMVbox = QtGui.QVBoxLayout()
        self.PMVbox.addLayout(self.PMHbox)
        self.horizontalLayout_3.addWidget(self.progressBar)

        self.verticalLayout_2.addLayout(self.PMVbox)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.horizontalLayout = QtGui.QHBoxLayout()

        self.Button_Cancel = QtGui.QPushButton("Cancel")
        self.centralWidget.addWidget(self.Button_Cancel)
        self.horizontalLayout.addWidget(self.Button_Cancel)

        self.Button_Display = QtGui.QPushButton("Display")
        self.centralWidget.addWidget(self.Button_Display)
        self.horizontalLayout.addWidget(self.Button_Display)
        # self.Button_Display.clicked.connect(self.Display)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        # set the signal  of  open IP file
        # self.Button_Open.clicked.connect(self.fileOpen)

        # set the signal of ScanIP
        self.list = []
        # self.work = ScanIP()
        self.thread = QtCore.QThread()
        # QtCore.QObject.connect(self.Button_ScanIP, QtCore.SIGNAL("clicked()"), self.ScanIP)
        self.n = 0
        self.cliked_index = 0
        self.listView_model = QtGui.QStandardItemModel(self.listView)

        # combobox and dataBase
        # self.comboBoxSetItem()
        # self.Button_OpenPath.clicked.connect(self.OpenPath)
        # self.Button_Cancel.clicked.connect(self.Cancel)

        # dislapy result on the window
        self.tableDisplayResultTable = QtGui.QTableWidget()
        self.TableHBox_T = QtGui.QVBoxLayout()
        self.TableHBox_T.addWidget(self.tableDisplayResultTable)
        self.displayResultLayout.addLayout(self.TableHBox_T, 0, 0)
        self.displayResultLayout.addLayout(self.TableHBox_B, 4, 0)
        header = ['IP', 'PORT', 'STATE', 'SERVICE', 'VERSION', 'PRODUCT', 'OS', 'TRACE', 'COORDINATE']
        self.tableDisplayResultTable.setColumnCount(9)
        self.tableDisplayResultTable.setHorizontalHeaderLabels(header)
        self.tableDisplayResultTable.setRowCount(50)



if __name__ == '__main__':
    app = QtGui.QApplication([])
    w = UiHomePage()
    app.exec_()