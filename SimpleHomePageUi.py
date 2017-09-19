# coding: utf-8
from PyQt4 import QtCore, QtGui
import sys
import logging

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

        # 添加log窗口
        self.log_HBoxLayout = QtGui.QHBoxLayout()
        self.log_TextBrower = QtGui.QTextBrowser()
        self.log_HBoxLayout.addWidget(self.log_TextBrower)
        self.central_widget.addLayout(self.log_HBoxLayout)
        XStream.stdout().messageWritten.connect(self.log_TextBrower.insertPlainText)
        XStream.stderr().messageWritten.connect(self.log_TextBrower.insertPlainText)

        # #　添加进度条
        # self.progressBar_HBoxLayout = QtGui.QHBoxLayout()
        # self.progressBar = QtGui.QProgressBar()
        # self.progressBar.setProperty("value", 0)
        # style = """
        #         QProgressBar {
        #             border: 2px solid grey;
        #             border-radius: 5px;
        #             text-align: center;
        #         }
        #
        #         QProgressBar::chunk {
        #             background-color: #88B0EB;
        #             width: 20px;
        #         }"""
        # self.progressBar.setStyleSheet(style)
        # self.progressBar_HBoxLayout.addWidget(self.progressBar)
        # self.central_widget.addLayout(self.progressBar_HBoxLayout)

        #　添加Start和Cancel按钮
        self.start_cancel_HBoxLayout = QtGui.QHBoxLayout()
        self.start_stop_button = QtGui.QPushButton("Start")
        self.start_cancel_HBoxLayout.addWidget(self.start_stop_button)
        self.start_stop_button.clicked.connect(self.click_start_stop_button)
        self.cancel_button = QtGui.QPushButton("Cancel")
        self.start_cancel_HBoxLayout.addWidget(self.cancel_button)
        self.cancel_button.clicked.connect(self.click_cancel_button)
        self.central_widget.addLayout(self.start_cancel_HBoxLayout)

    def click_start_stop_button(self):
        current_name = self.start_stop_button.text()
        if current_name == "Start":
            logger.info(QtCore.QString(u"开始截获数据包"))
            self.start_stop_button.setText("Finish")
        else:
            logger.info(QtCore.QString(u"停止截获数据包"))
            self.start_stop_button.setText("Start")
        # TODO:抓包并打标签为当时动作

    def click_cancel_button(self):
        logger.info(QtCore.QString(u"取消截获数据包"))
        self.start_stop_button.setText("Start")
        # TODO:把从上次点击开始按钮之后到现在收到的包都扔掉
        pass


class XStream(QtCore.QObject):
    """
    以下代码是抄来的，功能是把标准输入输出中打印的log做成信号和槽的模式，
    使得日志可以在UI中显示。
    """
    _stdout = None
    _stderr = None
    messageWritten = QtCore.pyqtSignal(str)

    def flush( self ):
        pass

    def fileno( self ):
        return -1

    def write( self, msg ):
        if ( not self.signalsBlocked() ):
            self.messageWritten.emit(unicode(msg))

    @staticmethod
    def stdout():
        if ( not XStream._stdout ):
            XStream._stdout = XStream()
            sys.stdout = XStream._stdout
        return XStream._stdout

    @staticmethod
    def stderr():
        if ( not XStream._stderr ):
            XStream._stderr = XStream()
            sys.stderr = XStream._stderr
        return XStream._stderr


class QtHandler(logging.Handler):
    def __init__(self):
        logging.Handler.__init__(self)

    def emit(self, record):
        record = self.format(record)
        if record: XStream.stdout().write('%s\n'%record)

# 设置log格式
logger = logging.getLogger(__name__)
handler = QtHandler()
handler.setFormatter(logging.Formatter('[%(asctime)s][%(levelname)s][%(filename)s:%(lineno)d]%(message)s'))
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

if __name__ == '__main__':
    app = QtGui.QApplication([])
    w = UiHomePage()
    app.exec_()