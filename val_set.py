# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'bit_config.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import copy
import sys
import shelve
# try:
# _fromUtf8 = QString.fromUtf8
# except AttributeError:
# def s):
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
    def setupUi(self, Dialog):
        # Dialog.setObjectName("Dialog"))
        Dialog.resize(492, 334)
        self.x = Dialog
        self.add_but = QPushButton(Dialog)
        self.add_but.setGeometry(QRect(390, 40, 75, 31))
        # self.add_but.setObjectName("add_but"))
        self.insert_but = QPushButton(Dialog)
        self.insert_but.setGeometry(QRect(390, 90, 75, 31))
        # self.insert_but.setObjectName("insert_but"))
        self.del_but = QPushButton(Dialog)
        self.del_but.setGeometry(QRect(390, 140, 75, 31))
        # self.del_but.setObjectName("del_but"))
        # self.edit_but = QPushButton(Dialog)
        # self.edit_but.setGeometry(QRect(390, 140, 75, 31))
        # self.edit_but.setObjectName("edit_but"))
        font = QFont()
        # font.setFamily("Courier"))
        font.setPointSize(12)

        self.namelabel = QLabel(Dialog)
        self.namelabel.setText("名 称：")
        self.namelabel.setGeometry(QRect(10, 10, 75, 31))
        self.namelabel.setFont(font)

        self.name = QLineEdit(Dialog)
        self.name.setGeometry(QRect(70, 10, 165, 25))
        self.name.setFont(font)

        self.dispchk = QCheckBox(Dialog)
        self.dispchk.setText("16进制显示值")
        self.dispchk.setGeometry(QRect(250, 10, 165, 25))

        self.tableWidget = QTableWidget(Dialog)
        self.tableWidget.setEnabled(True)
        self.tableWidget.setGeometry(QRect(10, 40, 351, 241))

        self.tableWidget.verticalHeader().setHidden(True)  # 隐藏行号
        # self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.setShowGrid(False)

        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy)
        # font = QFont()
        # font.setFamily("Courier"))
        font.setPointSize(10)

        self.tableWidget.setFont(font)
        self.tableWidget.setLayoutDirection(Qt.LeftToRight)
        self.tableWidget.setAutoFillBackground(False)
        self.tableWidget.setFrameShape(QFrame.Box)
        self.tableWidget.setFrameShadow(QFrame.Sunken)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setTabKeyNavigation(False)
        self.tableWidget.setProperty("showDropIndicator", False)
        self.tableWidget.setDragDropOverwriteMode(False)
        self.tableWidget.setShowGrid(True)
        self.tableWidget.setWordWrap(False)
        self.tableWidget.setCornerButtonEnabled(True)
        # self.tableWidget.setObjectName("tableWidget"))
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(0)
        item = QTableWidgetItem()
        item.setTextAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QTableWidgetItem()
        item.setTextAlignment(Qt.AlignLeft | Qt.AlignBottom)
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QTableWidgetItem()
        item.setTextAlignment(Qt.AlignLeft | Qt.AlignBottom)
        self.tableWidget.setHorizontalHeaderItem(2, item)

        self.tableWidget.setColumnWidth(0, 50)
        self.tableWidget.setColumnWidth(1, 100)
        self.tableWidget.setColumnWidth(2, 180)
        # self.tableWidget.setColumnWidth(3,110)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)

        self.tableWidget.verticalHeader().setHidden(True)  # 隐藏行号
        # self.tableWidget.setEditTriggers(QAbstractItemView.AllEditTriggers)  # 可编辑
        # print QAbstractItemView.AllEditTriggers,type(QAbstractItemView.AllEditTriggers)
        self.tableWidget.setEditTriggers(QAbstractItemView.DoubleClicked | QAbstractItemView.AnyKeyPressed)  # 可编辑

        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        # self.tableWidget.setShowGrid(False)

        # self.line = QFrame(Dialog)
        # self.line.setGeometry(QRect(10, 300, 351, 16))
        # self.line.setFrameShape(QFrame.HLine)
        # self.line.setFrameShadow(QFrame.Sunken)
        # self.line.setObjectName("line"))
        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QRect(110, 300, 156, 23))
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        # self.buttonBox.setObjectName("buttonBox"))
        # self.line_2 = QFrame(Dialog)
        # self.line_2.setGeometry(QRect(370, 10, 16, 251))
        # self.line_2.setFrameShape(QFrame.VLine)
        # self.line_2.setFrameShadow(QFrame.Sunken)
        # self.line_2.setObjectName("line_2"))

        # 信号与槽
        self.add_but.clicked.connect(self.add_fun)
        self.insert_but.clicked.connect(self.insert_fun)
        # self.edit_but.clicked.connect( self.edit_fun)
        self.del_but.clicked.connect(self.delete_fun)

        self.buttonBox.accepted.connect(self.confirm_fun)
        self.buttonBox.rejected.connect(self.exit_fun)

        self.dispchk.stateChanged.connect(self.valdisp)
        # 类成员
        self.row_count = 0  # 表的行数
        self.confirm_flag = False
        self.valSet_list = []
        self.valSet_dict = {}
        self.current_bitSet = {}
        self.choosename = None
        self.retranslateUi(Dialog)
        QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle("值域配置")
        self.add_but.setText("添 加")
        self.add_but.setShortcut(QKeySequence.SelectAll)
        self.add_but.setToolTip(u'Ctrl+A')

        self.insert_but.setText("插 入")
        self.insert_but.setShortcut(QKeySequence(u'Ctrl+I'))
        self.insert_but.setToolTip(u'Ctrl+I')

        self.del_but.setText("删 除")
        self.del_but.setShortcut(QKeySequence.Delete)
        self.del_but.setToolTip(u'Delete')
        # self.edit_but.setText("编 辑")
        self.tableWidget.setSortingEnabled(False)
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText("序号")
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText("值")
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText("描述")

    # 槽函数： add_but
    def add_fun(self):
        # print self.current_bitSet
        self.row_count += 1  # 行数加1
        self.tableWidget.setRowCount(self.row_count)
        self.tableWidget.setRowHeight(self.row_count - 1, 19)

        # print item.value(),type(item.value())
        item = QTableWidgetItem()
        item.setText(str(self.row_count))
        self.tableWidget.setItem(self.row_count - 1, 0, item)
        item = QTableWidgetItem()
        self.tableWidget.setItem(self.row_count - 1, 1, item)
        item = QTableWidgetItem()
        self.tableWidget.setItem(self.row_count - 1, 2, item)
        pass

    # 槽函数： insert_but
    def insert_fun(self):
        self.row_count += 1  # 行数加1
        new_row = self.tableWidget.currentRow()  #-1
        self.tableWidget.insertRow(new_row)
        # print self.tableWidget.currentRow()
        self.tableWidget.setRowHeight(new_row, 22)

        item = QSpinBox()
        item.setMinimum(0)
        item.setMaximum(31)
        # print item.value(),type(item.value())
        item = QTableWidgetItem()
        self.tableWidget.setItem(new_row, 0, item)
        item = QTableWidgetItem()
        self.tableWidget.setItem(new_row, 1, item)
        item = QTableWidgetItem()
        self.tableWidget.setItem(new_row, 2, item)
        for i in range(self.row_count):
            item = self.tableWidget.item(i, 0)
            item.setText(str(i + 1))
        pass

    # 槽函数： del_but
    def delete_fun(self):
        reply = QMessageBox.information(self.tableWidget, "提示", "确认删除？", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            row = self.tableWidget.currentRow()
            self.tableWidget.removeRow(row)
            self.row_count -= 1  # 行数减1
            for i in range(self.row_count):
                item = self.tableWidget.item(i, 0)
                item.setText(str(i + 1))
        pass

    # 槽函数： button_box
    def confirm_fun(self):
        name = self.name.text()
        # name=unicode(name)
        db_file = shelve.open('config', writeback=True)
        try:
            if self.choosename == name:
                pass
            else:
                if name in db_file['ValCfg_list']:
                    QMessageBox.warning(self.tableWidget, "错误", "与已有配置项重名，请修改！")
                    return
        except:
            pass
        self.confirm_flag = True
        row_count = self.tableWidget.rowCount()
        self.valSet_list = []
        self.valSet_dict = {}
        for i in range(row_count):
            value = self.tableWidget.item(i, 1).text()
            # value = QString(value).toUtf8()
            definition = self.tableWidget.item(i, 2).text()
            # definition = QString(definition).toUtf8()
            # definition = unicode(definition,'utf-8','ignore').encode('utf-8')
            try:
                value = eval(value)
                if value in self.valSet_list:
                    QMessageBox.warning(self.tableWidget, "错误",
                                        "第 " + str(i + 1) + " 行与第 " + str(self.valSet_list.index(value) + 1) + " 行值相同！")
                    return
            except:
                QMessageBox.warning(self.tableWidget, "错误", "第 " + str(i + 1) + " 行数据输入错误！")
                return
            # print bit_no,type(bit_no)
            self.valSet_dict[value] = definition
            self.valSet_list.append(value)
        # db_file= shelve.open('config.db',writeback=True)
        # print name
        if 'ValCfg_dict' in db_file.keys() and 'ValCfg_list' in db_file.keys():
            # print name
            if name in db_file['ValCfg_list']:
                db_file['ValCfg_dict'][name] = copy.deepcopy(self.valSet_dict)
            elif self.choosename is not None:
                ind = db_file['ValCfg_list'].index(self.choosename)
                db_file['ValCfg_list'][ind] = name
                db_file['ValCfg_dict'].pop(self.choosename)
                db_file['ValCfg_dict'][name] = copy.deepcopy(self.valSet_dict)
            else:
                db_file['ValCfg_list'].append(name)
                db_file['ValCfg_dict'][name] = copy.deepcopy(self.valSet_dict)
        else:
            db_file['ValCfg_list'] = []
            db_file['ValCfg_dict'] = {}
            db_file['ValCfg_list'].append(name)
            db_file['ValCfg_dict'][name] = copy.deepcopy(self.valSet_dict)
        # self.current_bitSet=copy.deepcopy(self.bitSet_dict)
        db_file.close()
        self.confirm_flag = True
        self.x.close()

    def exit_fun(self):
        # self.bitSet_list=[]
        # self.bitSet_dict=copy.deepcopy(self.current_bitSet)
        self.x.close()

    def UI_Reset(self):
        self.name.clear()
        self.choosename = None
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)
        self.row_count = 0

    def UI_Set(self, name):
        self.name.setText(name)
        self.choosename = name
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)  # 先清除表中内容，再按照当前行的位域设置进行显示
        self.row_count = 0
        # if self.bit_Dialog_cfg.current_bitSet!={} and self.bit_Dialog_cfg.current_bitSet!=None:
        db_file = shelve.open('config.db')
        # print name
        valSet = db_file['ValCfg_dict'][name]
        if valSet != None:
            # print self.bit_Dialog_cfg.current_bitSet
            # bitSet=cfg.current_bitSet
            # self.bit_Dialog_cfg.bitSet_dict=self.bit_Dialog_cfg.current_bitSet
            rowCount = len(valSet.keys())
            self.tableWidget.setRowCount(rowCount)
            self.row_count = rowCount
            index = 0
            x = valSet.keys()
            x = list(x)
            x.sort()  # 此处对字典的键值排序，按位从低到高显示
            for key in x:
                self.tableWidget.setRowHeight(index, 22)  # 先设置行高度
                item = QTableWidgetItem()
                item.setText(str(index + 1))
                self.tableWidget.setItem(index, 0, item)
                item = QTableWidgetItem()
                item.setText(str(key))
                self.tableWidget.setItem(index, 1, item)
                item = QTableWidgetItem()
                item.setText(valSet[key])
                self.tableWidget.setItem(index, 2, item)
                index += 1
        # self.bit_Dialog_cfg.current_bitSet={}   # 此处要清除，下次按新的位域设置显示位域编辑界面
        # self.bit_Dialog.show()
        pass

    def valdisp(self):
        x = self.dispchk.checkState()
        # print x
        if x == 2:
            for i in range(self.row_count):
                item = self.tableWidget.item(i, 1)
                value = item.text()
                # value = QString(value).toUtf8()
                # value = unicode(value,'utf-8','ignore').encode('utf-8')
                try:
                    value = eval(value)
                    vstring = '0x%X' % (value)
                except:
                    QMessageBox.warning(self.tableWidget, "错误", "第 " + str(i + 1) + " 行数据输入错误！")
                    # self.dispchk.setCheckState(0)
                    return
                item.setText(vstring)
        else:
            for i in range(self.row_count):
                item = self.tableWidget.item(i, 1)
                value = item.text()
                # value = QString(value).toUtf8()
                # value = unicode(value,'utf-8','ignore').encode('utf-8')
                try:
                    value = eval(value)
                    vstring = '%d' % (value)
                except:
                    QMessageBox.warning(self.tableWidget, "错误", "第 " + str(i + 1) + " 行数据输入错误！")
                    # self.dispchk.setCheckState(2)
                    return
                item.setText(vstring)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = QDialog(None)
    x = Ui_Dialog()
    x.setupUi(main)
    main.show()
    sys.exit(app.exec_())
    pass