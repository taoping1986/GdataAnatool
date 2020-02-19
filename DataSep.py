# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'fsfy.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
# try:
# _fromUtf8 = QString.fromUtf8
# except AttributeError:
# def _fromUtf8(s):
# return s
#
# try:
#     _encoding = QApplication.UnicodeUTF8
#     def _translate(context, text, disambig):
#         return QApplication.translate(context, text, disambig, _encoding)
# except AttributeError:
#     def _translate(context, text, disambig):
#         return QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def __init__(self):
        self.loopcnt = 0
        self.xscale = 0
        self.lpstart = 0
        self.lpend = 0
        self.colist = []
        self.confirm = False

    def setupUi(self, Dialog):
        self.x = Dialog
        # Dialog.setObjectName(u"分时复用解析设置")
        Dialog.resize(240, 200)
        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QRect(50, 155, 165, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        # self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.widget = QWidget(Dialog)
        self.widget.setGeometry(QRect(20, 20, 201, 130))
        # self.widget.setObjectName(_fromUtf8("widget"))
        self.gridLayout = QGridLayout(self.widget)
        # self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QLabel(self.widget)
        # self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.cnt = QLineEdit(self.widget)
        # self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.gridLayout.addWidget(self.cnt, 0, 1, 1, 1)
        self.label_2 = QLabel(self.widget)
        # self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.scale = QLineEdit(self.widget)
        # self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
        self.gridLayout.addWidget(self.scale, 1, 1, 1, 1)
        self.label_3 = QLabel(self.widget)
        # self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.start = QLineEdit(self.widget)
        # self.lineEdit_3.setObjectName(_fromUtf8("lineEdit_3"))
        self.gridLayout.addWidget(self.start, 2, 1, 1, 1)
        self.label_4 = QLabel(self.widget)
        # self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.end = QLineEdit(self.widget)
        # self.lineEdit_4.setObjectName(_fromUtf8("lineEdit_4"))
        self.gridLayout.addWidget(self.end, 3, 1, 1, 1)
        self.label_5 = QLabel(self.widget)
        self.gridLayout.addWidget(self.label_5, 4, 0, 1, 1)
        self.cols = QLineEdit(self.widget)
        self.gridLayout.addWidget(self.cols, 4, 1, 1, 1)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(self.confirmSlot)
        self.buttonBox.rejected.connect(Dialog.reject)
        QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(u"分时复用解析设置")
        self.label.setText(u"循环长度:")
        self.label_2.setText(u"时间轴分辨度:")
        self.label_3.setText(u"开始行:")
        self.label_4.setText(u"结束行:")
        self.label_5.setText(u"解析列号:")

    def confirmSlot(self):
        try:
            x = self.cnt.text()
            if x.strip() == '':
                QMessageBox.warning(self.buttonBox, u"错误", u'循环长度不能为空！')
                return
            else:
                self.loopcnt = eval(x.strip())
            x = self.scale.text().strip()
            if x != '':
                self.xscale = eval(x)
            x = self.start.text().strip()
            if x != '':
                self.lpstart = eval(x) - 1
            else:
                QMessageBox.warning(self.buttonBox, u"错误", u'开始行和结束行不能为空！')
                return
            x = self.end.text().strip()
            if x != '':
                self.lpend = eval(x) - 1
            else:
                QMessageBox.warning(self.buttonBox, u"错误", u'开始行和结束行不能为空！')
                return
            if self.lpend < self.lpstart:
                QMessageBox.warning(self.buttonBox, u"错误", u'开始行必须小于结束行！')
                return
            if self.lpend < 0 or self.lpstart < 0:
                QMessageBox.warning(self.buttonBox, u"错误", u'开始行和结束行必须大于0！')
                return
            x = self.cols.text()
            if x.strip() == '':
                QMessageBox.warning(self.buttonBox, u"错误", u'解析列号不能为空！')
                return
            else:
                self.colist = [eval(i) - 1 for i in x.split(',')]
                self.colist = list(set(self.colist))
                # print self.colist
        except:
            # QMessageBox.warning(self.)
            QMessageBox.warning(self.buttonBox, u"错误", u'输入含有非法字符！\n请检查!')
            return
            pass
        self.confirm = True
        self.x.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = QDialog(None)
    x = Ui_Dialog()
    x.setupUi(main)
    main.show()
    sys.exit(app.exec_())
    pass