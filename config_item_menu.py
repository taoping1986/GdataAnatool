# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'config_item_menu.ui'
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
    # def __init__(self):
    #     self.item_dict = {}
    #     self.item_list = {}
    def setupUi(self, Dialog):
        # Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(320, 399)
        font = QFont()
        font.setPointSize(12)
        Dialog.setFont(font)

        self.x = Dialog
        # self.bit_Dialog = QDialog(Dialog)
        # self.bit_Dialog_cfg = bit_set.Ui_Dialog()
        # self.bit_Dialog_cfg.setupUi(self.bit_Dialog)

        self.label = QLabel(Dialog)
        self.label.setGeometry(QRect(20, 30, 81, 21))
        font = QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        # self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QLabel(Dialog)
        self.label_2.setGeometry(QRect(20, 80, 81, 21))
        font = QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        # self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QLabel(Dialog)
        self.label_3.setGeometry(QRect(20, 130, 81, 21))
        font = QFont()
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        # self.label_3.setObjectName(_fromUtf8("label_3"))
        self.item_name = QLineEdit(Dialog)
        self.item_name.setGeometry(QRect(100, 30, 181, 20))
        font = QFont()
        font.setPointSize(12)
        self.item_name.setFont(font)
        self.item_name.setText("")
        # self.item_name.setObjectName(_fromUtf8("item_name"))
        self.item_style = QComboBox(Dialog)
        self.item_style.setGeometry(QRect(100, 80, 181, 22))
        font = QFont()
        font.setPointSize(12)
        self.item_style.setFont(font)
        # self.item_style.setObjectName(_fromUtf8("item_style"))
        self.item_style.addItem("")
        self.item_style.addItem("")
        self.item_style.addItem("")
        self.item_style.addItem("")
        self.item_style.addItem("")
        self.item_style.addItem("")
        self.item_style.addItem("")
        self.item_style.addItem("")
        self.item_style.addItem("")
        self.item_disp = QComboBox(Dialog)
        self.item_disp.setGeometry(QRect(100, 130, 181, 22))
        font = QFont()
        font.setPointSize(12)
        self.item_disp.setFont(font)
        # self.item_disp.setObjectName(_fromUtf8("item_disp"))
        self.item_disp.addItem("")
        self.item_disp.addItem("")
        self.label_4 = QLabel(Dialog)
        self.label_4.setGeometry(QRect(20, 180, 81, 21))
        font = QFont()
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        # self.label_4.setObjectName(_fromUtf8("label_4"))

        self.item_scale = QLineEdit(Dialog)
        self.item_scale.setGeometry(QRect(100, 180, 181, 20))
        font = QFont()
        font.setPointSize(12)
        self.item_scale.setFont(font)
        self.item_scale.setText("")
        # self.item_scale.setObjectName(_fromUtf8("item_name"))
        self.item_scale.setText('1.000000')

        self.label_7 = QLabel(Dialog)
        self.label_7.setGeometry(QRect(20, 220, 81, 21))
        font = QFont()
        font.setPointSize(12)
        self.label_7.setFont(font)
        self.label_7.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        # self.label_7.setObjectName(_fromUtf8("label_7"))
        self.spinBox = QSpinBox(Dialog)
        self.spinBox.setGeometry(QRect(100, 220, 42, 22))
        self.spinBox.setMinimum(1)
        # self.spinBox.setObjectName(_fromUtf8("spinBox"))
        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QRect(100, 310, 156, 23))
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        # self.buttonBox.setObjectName(_fromUtf8("buttonBox"))


        self.line = QFrame(Dialog)
        self.line.setGeometry(QRect(20, 280, 281, 16))
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        # self.line.setObjectName(_fromUtf8("line2"))

        # self.bit_check = QCheckBox(Dialog)
        # self.bit_check.setText(_fromUtf8(""))
        # self.bit_check.setObjectName(_fromUtf8("bit_check"))
        # self.bit_check.setGeometry(QRect(100, 183, 16, 16))
        #
        # self.bit_edit_but = QToolButton(Dialog)
        # self.bit_edit_but.setEnabled(False)
        # self.bit_edit_but.setObjectName(_fromUtf8("bit_edit_but"))
        # self.bit_edit_but.setGeometry(QRect(120, 180, 47, 22))

        # self.bit_check.hide()
        # self.bit_edit_but.hide()

        # self.label_5 = QLabel(Dialog)
        # font = QFont()
        # font.setPointSize(9)
        # self.label_5.setFont(font)
        # self.label_5.setObjectName(_fromUtf8("label_5"))
        # self.label_5.setGeometry(QRect(173, 180, 48, 22))

        # self.nums_check = QCheckBox(Dialog)
        # self.nums_check.setText(_fromUtf8(""))
        # self.nums_check.setObjectName(_fromUtf8("nums_check"))
        # self.nums_check.setGeometry(QRect(100, 215, 16, 16))
        #
        # self.nums_edit_but = QToolButton(Dialog)
        # self.nums_edit_but.setEnabled(False)
        # self.nums_edit_but.setObjectName(_fromUtf8("nums_edit_but"))
        # self.nums_edit_but.setGeometry(QRect(120, 213, 47, 22))

        self.label_6 = QLabel(Dialog)
        font = QFont()
        font.setPointSize(9)
        self.label_6.setFont(font)
        # self.label_6.setObjectName(_fromUtf8("label_6"))
        self.label_6.setGeometry(QRect(173, 213, 60, 22))

        # 信号与槽函数
        self.buttonBox.accepted.connect(self.confirm_fun)
        self.buttonBox.rejected.connect(Dialog.close)
        # 20170814  设置选择为浮点数时，只能解析显示为10进制
        self.item_style.currentIndexChanged.connect(self.item_style_changeslot)
        # self.bit_check, SIGNAL(_fromUtf8("stateChanged(int)")), self.bitCheck_fun)
        # self.nums_check, SIGNAL(_fromUtf8("stateChanged(int)")), self.numCheck_fun)

        # self.bit_edit_but, SIGNAL(_fromUtf8("clicked()")), self.bitSet_fun)
        # self.nums_edit_but, SIGNAL(_fromUtf8("clicked()")), self.numsSet_fun)

        # self.bit_Dialog, SIGNAL(_fromUtf8("rejected()")), self.bitSet_get)


        # 类成员，用于信息传递
        self.confirm_flag = False
        self.it_name = None
        self.it_name_chkList = []  # 用于检查输入的“名称”是否与当前表中数据项重名
        self.it_add_flag = False  # 上层界面的“添加”“插入”按钮触发该标志为True，用于检测是否重名
        self.it_style = None
        self.it_disp = None
        self.it_scale = 1.0
        self.it_bitChk = False
        self.it_numChk = False
        self.it_addNum = 1
        self.it_bitSet = {}
        self.it_numSet = {}

        self.retranslateUi(Dialog)
        QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle("Dialog")
        self.label.setText(u"名 称：")
        self.label_2.setText(u"数据类型：")
        self.label_3.setText(u"显示方式：")
        self.item_style.setItemText(0, u"32位 无符号 整型")
        self.item_style.setItemText(1, u"32位 有符号 整型")
        self.item_style.setItemText(2, u"32位 浮点型")
        self.item_style.setItemText(3, u"40位 浮点型")
        self.item_style.setItemText(4, u"64位 浮点型")
        self.item_style.setItemText(5, u"16位 无符号 整型")
        self.item_style.setItemText(6, u"16位 有符号 整型")
        self.item_style.setItemText(7, u"8位  无符号 整型")
        self.item_style.setItemText(8, u"8位  有符号 整型")
        self.item_disp.setItemText(0, u"DEC 显示")
        self.item_disp.setItemText(1, u"HEX 显示")
        self.label_4.setText(u"画图比例：")
        self.label_7.setText(u"添加数量：")
        # self.bit_edit_but.setText(_translate("Dialog", "...", None))
        # self.label_5.setText(_translate("Dialog", "位域编辑", None))
        # self.nums_edit_but.setText(_translate("Dialog", "...", None))
        # self.label_6.setText(_translate("Dialog", "值域集编辑", None))

    # 确定按钮  槽函数
    def confirm_fun(self):
        # 重名检查
        self.it_name = self.item_name.text()
        self.it_addNum = self.spinBox.value()
        # 20170904 修改重名检测策略，在添加多项时，连同自动生成的名称一起检查
        nameTemp = [self.it_name]
        for i in range(self.it_addNum - 1): nameTemp.append(self.it_name + '_' + str(i + 1))
        # print nameTemp
        if self.it_add_flag:  # 在上层界面为添加、插入按钮时检测是否重名
            for n in nameTemp:
                if n in self.it_name_chkList:
                    QMessageBox.warning(self.item_name, u"错误", u"“名称”重复，请重新设置！")
                    return

        self.it_scale = self.item_scale.text()
        try:
            self.it_scale = eval(self.it_scale)
        except:
            QMessageBox.warning(self.item_name, u"错误", u"画图量纲设置错误！")
            return
        self.confirm_flag = True
        self.it_style = self.item_style.currentIndex()
        # print self.it_style
        self.it_disp = self.item_disp.currentIndex()
        # self.it_addNum = self.spinBox.value()
        self.x.close()
        # print self.it_addNum
        # if self.bit_check.checkState()==2:
        #     (self.it_bitChk,self.it_numChk)=(True,False)
        #     # self.it_numChk=False
        # elif self.nums_check.checkState()==2:
        #     (self.it_bitChk,self.it_numChk)=(False,True)
        #     # self.it_numChk=True
        # else:
        #     (self.it_bitChk,self.it_numChk)=(False,False)
        # self.it_bitChk=False
        # self.it_numChk=False


    # def exit_fun(self):
    #     pass

    # 位域编辑选择 槽函数  bit_check
    # def bitCheck_fun(self):
    #     if self.bit_check.checkState()==2:
    #         self.bit_edit_but.setDisabled(False)
    #         self.nums_check.setCheckState(0)
    #         self.nums_edit_but.setDisabled(True)
    #     else:
    #         self.bit_edit_but.setDisabled(True)

    # 值域集编辑选择 槽函数  nums_check
    # def numCheck_fun(self):
    #     if self.nums_check.checkState()==2:
    #         self.nums_edit_but.setDisabled(False)
    #         self.bit_check.setCheckState(0)
    #         self.bit_edit_but.setDisabled(True)
    #     else:
    #         self.nums_edit_but.setDisabled(True)


    # 位域编辑 槽函数  bit_edit_but
    # def bitSet_fun(self):
    #     self.bit_Dialog_cfg.tableWidget.setRowCount(0)         # 先清除表中内容，再按照当前行的位域设置进行显示
    #     self.bit_Dialog_cfg.row_count=0
    #     if self.bit_Dialog_cfg.current_bitSet!={} and self.bit_Dialog_cfg.current_bitSet!=None:
    #         print self.bit_Dialog_cfg.current_bitSet
    #         bitSet=self.bit_Dialog_cfg.current_bitSet
    #         self.bit_Dialog_cfg.bitSet_dict=self.bit_Dialog_cfg.current_bitSet
    #         rowCount=len(bitSet.keys())
    #         self.bit_Dialog_cfg.tableWidget.setRowCount(rowCount)
    #         self.bit_Dialog_cfg.row_count=rowCount
    #         index=0
    #         x = bitSet.keys()
    #         x.sort()                # 此处对字典的键值排序，按位从低到高显示
    #         for key in x:
    #             self.bit_Dialog_cfg.tableWidget.setRowHeight(index,17)  # 先设置行高度
    #             item = QSpinBox()
    #             item.setMinimum(0)
    #             item.setMaximum(31)
    #             item.setValue(key)
    #             self.bit_Dialog_cfg.tableWidget.setCellWidget(index,0, item)
    #             item = QTableWidgetItem()
    #             item.setText(_translate("Dialog", bitSet[key][1], None))
    #             self.bit_Dialog_cfg.tableWidget.setItem(index,1, item)
    #             item = QTableWidgetItem()
    #             item.setText(_translate("Dialog", bitSet[key][0], None))
    #             self.bit_Dialog_cfg.tableWidget.setItem(index,2, item)
    #             index+=1
    #     # self.bit_Dialog_cfg.current_bitSet={}   # 此处要清除，下次按新的位域设置显示位域编辑界面
    #     self.bit_Dialog.show()
    #     pass

    # def numsSet_fun(self):
    #     pass
    # 20170814  设置选择为浮点数时，只能解析显示为10进制
    def item_style_changeslot(self):
        if self.item_style.currentIndex() in [2, 3, 4]:
            self.item_disp.setCurrentIndex(0)
            self.item_disp.setDisabled(True)
        else:
            self.item_disp.setDisabled(False)


            # def slottest(self):
            #     print self.item_style.currentIndex()
            #     print "slop triggered!"


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = QDialog(None)
    x = Ui_Dialog()
    x.setupUi(main)
    main.show()
    sys.exit(app.exec_())
    pass