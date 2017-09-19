# coding: utf-8
from PyQt4 import QtCore, QtGui

class UiHomePage(QtGui.QWidget):
    def __init__(self, parent=None):
        super(UiHomePage, self).__init__()
        self.setup_ui()
        self.show()
        self.raise_()

    def setup_ui(self):
        # 设置窗口大小为最小
        self.showMinimized()
        self.central_widget = QtGui.QVBoxLayout()

        # 设置全局的layout
        self.setLayout(self.central_widget)

        #　添加一个显示日志的ListView
        self.log_HBoxLayout = QtGui.QHBoxLayout()
        self.log_ListView = QtGui.QListView()
        self.log_HBoxLayout.addWidget(self.log_ListView)
        self.log_ListView.setSpacing(4)
        self.central_widget.addLayout(self.log_HBoxLayout)

        #　添加进度条
        self.progressBar_HBoxLayout = QtGui.QHBoxLayout()
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
        self.progressBar_HBoxLayout.addWidget(self.progressBar)
        self.central_widget.addLayout(self.progressBar_HBoxLayout)

        #　添加Start和Cancel按钮
        self.start_cancel_HBoxLayout = QtGui.QHBoxLayout()
        self.start_stop_button = QtGui.QPushButton("Start")
        self.start_cancel_HBoxLayout.addWidget(self.start_stop_button)
        self.start_stop_button.clicked.connect(self.click_start_stop_button)
        self.cancel_button = QtGui.QPushButton("Cancel")
        self.start_cancel_HBoxLayout.addWidget(self.cancel_button)
        self.central_widget.addLayout(self.start_cancel_HBoxLayout)

    def click_start_stop_button(self):
        currentName = self.start_stop_button.text()
        if currentName == "Start":
            self.start_stop_button.setText("Finish")
        else:
            self.start_stop_button.setText("Start")

if __name__ == '__main__':
    app = QtGui.QApplication([])
    w = UiHomePage()
    app.exec_()