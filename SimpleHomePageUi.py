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

        #　添加一个显示日志的ListView
        self.logHBoxLayout = QtGui.QHBoxLayout()
        self.loglistView = QtGui.QListView()
        self.logHBoxLayout.addWidget(self.loglistView)
        self.loglistView.setSpacing(4)
        self.centralWidget.addLayout(self.logHBoxLayout)
        # self.listView.clicked.connect(self.on_listView_cliked)

        #　添加进度条
        self.progressBarHBoxLayout = QtGui.QHBoxLayout()
        self.progressBar = QtGui.QProgressBar()
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
        self.progressBarHBoxLayout.addWidget(self.progressBar)
        self.centralWidget.addLayout(self.progressBarHBoxLayout)

        #　添加Start和Cancel按钮
        self.StartAndCancelHBoxLayout = QtGui.QHBoxLayout()
        self.Button_Cancel = QtGui.QPushButton("Start")
        self.StartAndCancelHBoxLayout.addWidget(self.Button_Cancel)
        self.Button_Display = QtGui.QPushButton("Cancel")
        self.StartAndCancelHBoxLayout.addWidget(self.Button_Display)
        # self.Button_Display.clicked.connect(self.Display)
        self.centralWidget.addLayout(self.StartAndCancelHBoxLayout)

if __name__ == '__main__':
    app = QtGui.QApplication([])
    w = UiHomePage()
    app.exec_()