# -*- coding:UTF-8 -*-

from PyQt5.QtWidgets import QWidget, QLineEdit, QFormLayout, QPushButton, QApplication
from PyQt5.QtGui import QIntValidator, QFont
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from main import Amazon
import sys, time, random


class RunThread(QThread):
    trigger = pyqtSignal(str)

    def __init__(self, parent=None):
        super(RunThread, self).__init__()
        self.setObjectName('spider')
        self.time_wait_1 = 0
        self.time_wait_2 = 0

    def __del__(self):
        self.wait()

    def save_result(self, result):
        with open('txffc.txt', 'w', encoding='utf-8') as f:
            f.write(result)

    def run(self):
        #print('run ...')
        last_res = ''
        while True:
            time.sleep(self.time_wait_2)
            result = Amazon(5).go()
            result_str = ''
            if result != None:
                result_str = " ".join(result)
            print(result_str)
            if result_str != '' and result_str != last_res:
                self.trigger.emit(result_str)
                self.save_result(result_str)
                last_res = result_str
            self.time_wait_1 = random.randint(0,4) + random.random()
            self.time_wait_2 = 5 - self.time_wait_1
            time.sleep(self.time_wait_1)

class lineEditDemo(QWidget):
    def __init__(self,parent=None):
        super(lineEditDemo, self).__init__(parent)

        #self.setFixedSize(*(400,100))

        #创建文本
        self.e1=QLineEdit()
        #设置文本校验器为整数，只有输入整数才为有效值
        self.e1.setValidator(QIntValidator())
        #设置文本靠右对齐
        self.e1.setAlignment(Qt.AlignCenter)
        #设置文本的字体和字号大小
        self.e1.setFont(QFont('Arial',20))

        self.e1.setReadOnly(True)

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
        self.thread = RunThread()
        self.thread.trigger.connect(self.txtUpdate)
        self.thread.start()

    def txtUpdate(self, str):
        #print('result: ' + str)
        self.e1.setText(str)
        #QApplication.processEvents()

    def closeEvent(self, event):
        sys.exit(app.exec_())


if __name__ == '__main__':
    app=QApplication(sys.argv)
    win=lineEditDemo()
    win.show()
    sys.exit(app.exec_())
