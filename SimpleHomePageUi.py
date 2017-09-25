# coding: utf-8
from PyQt4 import QtCore, QtGui
from PacketCapturer import PacketCapturer
import sys
import logging


class UiHomePage(QtGui.QWidget):
    def __init__(self, parent=None):
        super(UiHomePage, self).__init__()
        self.setup_ui()
        self.show()
        self.raise_()

        # 启动抓包线程
        self.packet_capturer = PacketCapturer()
        self.packet_capturer.start()

    def setup_ui(self):
        """
        建立UI界面
        """
        # 设置窗口大小为最小
        self.showMinimized()
        self.central_widget = QtGui.QVBoxLayout()

        # 设置全局的layout
        self.setLayout(self.central_widget)

        # 添加log窗口
        self.log_HBoxLayout = QtGui.QHBoxLayout()
        self.log_TextBrower = QtGui.QTextBrowser()
        QtCore.QObject.connect(self.log_TextBrower, QtCore.SIGNAL("cursorPositionChanged()"), self.auto_scroll)
        self.log_HBoxLayout.addWidget(self.log_TextBrower)
        self.central_widget.addLayout(self.log_HBoxLayout)
        XStream.stdout().messageWritten.connect(self.log_TextBrower.insertPlainText)
        # XStream.stderr().messageWritten.connect(self.log_TextBrower.insertPlainText)

        # 添加一个UI的label
        self.label_HBoxLayout = QtGui.QHBoxLayout()
        self.label = QtGui.QLabel(QtCore.QString(u"请选择接下来要做的动作："))
        self.label_HBoxLayout.addWidget(self.label)
        self.central_widget.addLayout(self.label_HBoxLayout)

        # 添加一些单选框
        moods = [
            QtGui.QRadioButton("open weibo"),
            QtGui.QRadioButton("send weibo"),
            QtGui.QRadioButton("like weibo"),
            QtGui.QRadioButton("forward weibo"),
            QtGui.QRadioButton("refresh weibo"),
            QtGui.QRadioButton("profile weibo"),
            QtGui.QRadioButton("comment weibo")
        ]
        self.moods_HBoxLayout = QtGui.QHBoxLayout()
        self.mood_button_group = QtGui.QButtonGroup()
        for i, mood in enumerate(moods):
            self.moods_HBoxLayout.addWidget(mood)
            self.mood_button_group.addButton(mood, i)
            mood.clicked.connect(self.radio_button_clicked)
        self.central_widget.addLayout(self.moods_HBoxLayout)

        #　添加Start和Cancel按钮
        self.start_cancel_HBoxLayout = QtGui.QHBoxLayout()
        self.start_stop_button = QtGui.QPushButton("Start")
        self.start_cancel_HBoxLayout.addWidget(self.start_stop_button)
        self.start_stop_button.clicked.connect(self.click_start_stop_button)
        self.cancel_button = QtGui.QPushButton("Cancel")
        self.start_cancel_HBoxLayout.addWidget(self.cancel_button)
        self.cancel_button.clicked.connect(self.click_cancel_button)
        self.central_widget.addLayout(self.start_cancel_HBoxLayout)

    def auto_scroll(self):
        """
        实现log自动滚动
        """
        max = self.log_TextBrower.verticalScrollBar().maximum()
        self.log_TextBrower.verticalScrollBar().setValue(max)

    def radio_button_clicked(self):
        """
        单选框被选中时执行
        """
        self.label = self.mood_button_group.checkedButton().text()
        logger.debug(QtCore.QString(u"当前数据流标签为： %s" % self.label))

    def click_start_stop_button(self):
        current_name = self.start_stop_button.text()
        if current_name == "Start":
            if not self.mood_button_group.checkedButton():
                QtGui.QMessageBox.warning(self, "",
                                          QtCore.QString(u"请选择标签！"),
                                          QtGui.QMessageBox.Cancel, QtGui.QMessageBox.NoButton,
                                          QtGui.QMessageBox.NoButton)
                return
            logger.info(QtCore.QString(u"开始截获数据包"))
            self.start_stop_button.setText("Finish")

            # 开始抓包
            self.packet_capturer.enable_capture()
        else:
            logger.info(QtCore.QString(u"停止截获数据包"))
            self.packet_capturer.dump_packets(self.label)
            self.start_stop_button.setText("Start")

            # 停止抓包
            self.packet_capturer.disable_capture()
        # TODO:抓包并打标签为当时动作

    def click_cancel_button(self):
        logger.info(QtCore.QString(u"取消截获数据包"))
        self.packet_capturer.disable_capture()
        self.start_stop_button.setText("Start")
        # 把选中的标签去掉
        mood = self.mood_button_group.checkedButton()
        if mood:
            # 一定要这么写才能把选中的单选框去掉
            self.mood_button_group.setExclusive(False)
            mood.setChecked(False)
            self.mood_button_group.setExclusive(True)

        # 把从上次点击开始按钮之后到现在收到的包都扔掉
        self.packet_capturer.drop_packets()


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
logger = logging.getLogger("log")
handler = QtHandler()
handler.setFormatter(logging.Formatter('[%(asctime)s][%(levelname)s][%(filename)s:%(lineno)d]%(message)s'))
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

if __name__ == '__main__':
    app = QtGui.QApplication([])
    # 添加这一行代码后，即使用sudo启动界面也不会变丑了
    app.setStyle("gtk")
    w = UiHomePage()
    app.exec_()