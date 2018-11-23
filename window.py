# -*- coding:UTF-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from main import  Amazon
import sys, time


class RunThread(QThread):
    trigger = pyqtSignal(str)

    def __init__(self, parent=None):
        super(RunThread, self).__init__()
        self.setObjectName('spider')

    def __del__(self):
        self.wait()

    def run(self):
        while True:
            restlt = Amazon(5).go()
            self.trigger.emit(restlt)
            time.sleep(5)

class lineEditDemo(QWidget):
    def __init__(self,parent=None):
        super(lineEditDemo, self).__init__(parent)

        #创建文本
        self.e1=QLineEdit()
        #设置文本校验器为整数，只有输入整数才为有效值
        self.e1.setValidator(QIntValidator())
        #设置文本靠右对齐
        self.e1.setAlignment(Qt.AlignCenter)
        #设置文本的字体和字号大小
        self.e1.setFont(QFont('Arial',20))

        #表单布局
        flo=QFormLayout()
        #添加名称及控件到布局中
        flo.addRow('预测结果：',self.e1)

        self.btn = QPushButton('start')

        self.btn.clicked.connect(self.work)

        flo.addRow(self.btn)

        #设置窗口的布局
        self.setLayout(flo)

        self.setWindowTitle("Demo")

    def work(self):
        print('btn clicked')
        self.thread = RunThread()
        self.thread.trigger.connect(self.txtUpdate)
        self.thread.run()

    def txtUpdate(self, str):
        print('slot run: ' + str)
        self.e1.setText(str)


if __name__ == '__main__':
    app=QApplication(sys.argv)
    win=lineEditDemo()
    win.show()
    sys.exit(app.exec_())
