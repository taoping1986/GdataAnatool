# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'config_menu3.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

# from PyQt4 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys, os, shelve, copy
import config_set_menu

from docx import Document

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
        self.frame_dict = {}
        self.frame_list = []
        if os.path.exists('config.dat'):
            db_file = shelve.open('config')
            if 'frame_dict' in db_file.keys() and 'frame_list' in db_file.keys():
                self.frame_dict = db_file['frame_dict']
                self.frame_list = db_file['frame_list']
        self.but_switch = 0  # 按键检测：1-添加  2-编辑  0-其他
        self.current_config = None
        self.confirm_flag = False
        self.multiItems = False
        self.config_out = None  # 选择的配置通过该变量传出
        self.config_out_list = []
        self.item_select_list = []
        self.item_select_name_list = []
        pass

    def setupUi(self, Dialog):
        # Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(341, 478)
        self.x = Dialog

        self.new_config = QDialog(Dialog)  # 配置项编辑的子界面
        self.new = config_set_menu.Ui_Dialog()
        self.new.setupUi(self.new_config)

        self.listWidget = QListWidget(Dialog)
        self.listWidget.setGeometry(QRect(10, 20, 201, 401))
        # self.listWidget.setSelectionModel(QAbstractItemView.ExtendedSelection)
        self.listWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        # self.listWidget.setObjectName(_fromUtf8("listWidget"))

        self.add_but = QPushButton(Dialog)
        self.add_but.setGeometry(QRect(240, 20, 75, 31))
        # self.add_but.setObjectName(_fromUtf8("add_but"))
        self.del_but = QPushButton(Dialog)
        self.del_but.setGeometry(QRect(240, 70, 75, 31))
        # self.del_but.setObjectName(_fromUtf8("del_but"))
        self.del_but.setDisabled(True)
        self.edit_but = QPushButton(Dialog)
        self.edit_but.setGeometry(QRect(240, 120, 75, 31))
        # self.edit_but.setObjectName(_fromUtf8("edit_but"))
        self.edit_but.setDisabled(True)
        self.copy_but = QPushButton(Dialog)
        self.copy_but.setGeometry(QRect(240, 170, 75, 31))
        # self.copy_but.setObjectName(_fromUtf8("copy_but"))
        self.copy_but.setDisabled(True)
        self.download_but = QPushButton(Dialog)
        self.download_but.setGeometry(QRect(240, 220, 75, 31))
        # self.download_but.setObjectName(_fromUtf8("download_but"))
        self.download_but.setDisabled(True)
        self.confirm_but = QPushButton(Dialog)
        self.confirm_but.setGeometry(QRect(240, 340, 75, 31))
        # self.confirm_but.setObjectName(_fromUtf8("confirm_but"))
        self.confirm_but.setDisabled(True)
        self.exit_but = QPushButton(Dialog)
        self.exit_but.setGeometry(QRect(240, 390, 75, 31))
        # self.exit_but.setObjectName(_fromUtf8("exit_but"))

        self.add_but.clicked.connect(self.add_config)
        self.new_config.rejected.connect(self.add_item)  # 添加新的帧格式
        self.edit_but.clicked.connect(self.edit_config)  # 20170816 修改bug  self.new_config.show->self.edit_config

        self.listWidget.itemSelectionChanged.connect(
            self.itemSelected)  #, SIGNAL("itemSelectionChanged()"), self.itemSelected)
        self.listWidget.itemDoubleClicked.connect(self.edit_config)

        self.del_but.clicked.connect(self.item_delete)
        self.copy_but.clicked.connect(self.item_saveas)

        self.download_but.clicked.connect(self.item_download)

        self.confirm_but.clicked.connect(self.confirm)
        self.exit_but.clicked.connect(Dialog.close)

        # QObject.connect(self.listWidget, SIGNAL(_fromUtf8("itemSelectionChanged()")), self.choosed_func)

        for x in self.frame_list:
            item = QListWidgetItem()
            font = QFont()
            font.setPointSize(12)
            item.setFont(font)
            item.setText(x)
            self.listWidget.addItem(item)

        self.retranslateUi(Dialog)
        QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(u"数据格式选择")
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        # item = self.listWidget.item(0)
        # item.setText(_translate("Dialog", "设置项", None))
        self.listWidget.setSortingEnabled(__sortingEnabled)
        self.add_but.setText(u"添 加")
        self.add_but.setShortcut(QKeySequence.SelectAll)
        self.add_but.setToolTip(u'Ctrl+A')

        self.del_but.setText(u"删 除")
        self.del_but.setShortcut(QKeySequence.Delete)
        self.del_but.setToolTip(u'Delete')

        self.edit_but.setText(u"编 辑")

        self.copy_but.setText(u"另 存")
        self.copy_but.setShortcut(QKeySequence.Save)
        self.copy_but.setToolTip(u'Ctrl+s')

        self.download_but.setText(u"导 出")

        self.confirm_but.setText(u"确 认")
        self.confirm_but.setDefault(True)
        self.exit_but.setText(u"退 出")

    # 添加按钮槽函数
    def add_config(self):
        self.but_switch = 1  # 添加按钮触发
        self.new.UI_Reset()
        self.new_config.show()

    # 编辑按钮槽函数
    def edit_config(self):
        self.but_switch = 2  # 编辑按钮触发
        self.UI_Set(self.frame_dict[self.item_select_name])
        self.new_config.show()

    # 设置界面退出槽函数
    def add_item(self):
        # 添加新配置项
        if self.new.confirm == True and self.but_switch == 1:
            # name = unicode(self.new.Frame_name.text())#.encode('utf-8')
            name = self.new.Frame_name.text()  #.encode('utf-8')
            # text = self.new.Frame_name.text()
            # print self.frame_dict.keys()
            # if unicode(self.new.Frame_name.text()) in self.frame_dict.keys():
            if self.new.Frame_name.text() in self.frame_dict.keys():
                name += u'__rename'
                i = 1
                while name in self.frame_list:
                    name = name[:name.rfind('__rename') + 8] + str(i)
                    i += 1
                QMessageBox.information(self.add_but, u"提示", u"已存在同名项，自动更名为:\n")

            item = QListWidgetItem()
            font = QFont()
            font.setPointSize(12)
            item.setFont(font)
            # item.setText(self.new.Frame_name.text())
            item.setText(name)
            self.listWidget.addItem(item)
            new_item = frame_style(name)
            # if self.new.head_chked:
            #     new_item.head_chked=True
            new_item.frame_head = self.new.f_head
            # if self.new.tail_chked:
            #     new_item.tail_chked=True
            new_item.frame_endian = self.new.f_endian
            # if self.new.trans_chked:
            #     new_item.trans_chked=True
            #     new_item.frame_trans=self.new.trans

            new_item.frame_datCfg_dict = copy.deepcopy(self.new.item_dict)
            new_item.frame_datCfg_list = copy.deepcopy(self.new.item_list)

            self.frame_dict[name] = new_item
            # self.frame_list.append(unicode(item.text()))
            self.frame_list.append(item.text())
            self.new.confirm = False
        # 回写选中的配置项
        elif self.new.confirm == True and self.but_switch == 2:
            self.f_writeback()

    # 删除按钮槽函数
    def item_delete(self):
        reply = QMessageBox.information(self.listWidget, u"提示", u"确认删除？", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.item_select = self.listWidget.item(self.listWidget.currentRow())
            name = self.item_select.text()
            # name = unicode(name)#unicode(name,'utf-8','ignore').encode('utf-8')
            self.listWidget.takeItem(self.listWidget.currentRow())
            self.frame_dict.pop(name)
            self.frame_list.remove(name)
            if len(self.frame_list) == 0:
                self.del_but.setDisabled(True)
                self.edit_but.setDisabled(True)
                self.copy_but.setDisabled(True)
                self.confirm_but.setDisabled(True)
        else:
            return

    # 另存按钮槽函数
    def item_saveas(self):
        item = QListWidgetItem()
        font = QFont()
        font.setPointSize(12)
        item.setFont(font)
        self.item_select = self.listWidget.item(self.listWidget.currentRow())
        name = self.item_select.text()
        # name = unicode(name)#unicode(name,'utf-8','ignore').encode('utf-8')
        index = 1
        name_temp = name
        while name_temp in self.frame_list:
            name_temp = name + u'复件' + str(index)
            index += 1
            item.setText(name_temp)
        self.listWidget.addItem(item)
        new_item = copy.deepcopy(self.frame_dict[name])
        new_name = item.text()  #unicode(item.text(),'utf-8','ignore').encode('utf-8')
        new_item.frame_name = new_name
        self.frame_dict[new_name] = new_item
        self.frame_list.append(new_name)

    # 导出按钮槽函数
    def item_download(self):
        self.item_select = self.listWidget.item(self.listWidget.currentRow())
        name = self.item_select.text()
        # name = unicode(name)#unicode(name,'utf-8','ignore').encode('utf-8')
        file = QFileDialog.getSaveFileName(filter=u'Word(*.docx);;')[0]
        if file == '':
            return
        # print file,type(file)
        doc = Document(r'filemod\cfgDownload.docx')
        resTable = doc.tables[0]
        item_dict = self.frame_dict[name].frame_datCfg_dict
        sty_dict = {0: 'UINT32', 1: 'INT32', 2: 'FLOAT32', 3: 'FLOAT40',
                    4: 'FLOAT64', 5: 'UINT16', 6: 'INT16', 7: 'UINT8', 8: 'INT8'}
        dis_dict = {0: 'DEC', 1: 'HEX'}
        index = 0
        for item in self.frame_dict[name].frame_datCfg_list:
            index += 1
            new = resTable.add_row()
            cells = new.cells
            cells[0].text = str(index)
            cells[1].text = item_dict[item].name
            cells[2].text = sty_dict[item_dict[item].dataStyle]
            cells[3].text = dis_dict[item_dict[item].disp]
            cells[4].text = str(item_dict[item].scale)
        doc.save(file)
        print('>> Download Success!(%s)' % (file))

    # 列表选项选择槽函数
    def itemSelected(self):
        self.del_but.setDisabled(False)
        self.edit_but.setDisabled(False)
        self.copy_but.setDisabled(False)
        self.download_but.setDisabled(False)
        self.confirm_but.setDisabled(False)
        self.item_select = self.listWidget.item(self.listWidget.currentRow())
        if self.item_select == None:
            self.del_but.setDisabled(True)
            self.edit_but.setDisabled(True)
            self.copy_but.setDisabled(True)
            self.confirm_but.setDisabled(True)
            return
        name = self.item_select.text()
        self.item_select_name = name  #unicode(name,'utf-8','ignore').encode('utf-8')

    # 确定按钮槽函数
    def confirm(self):
        self.confirm_flag = True
        items = self.listWidget.selectedItems()
        if len(items) == 1:
            self.item_select = self.listWidget.item(self.listWidget.currentRow())
            self.item_select_name = self.item_select.text()
            self.config_out = copy.deepcopy(self.frame_dict[self.item_select_name])
            self.x.close()
        else:
            self.multiItems = True
            self.item_select_name_list = []
            self.config_out_list = []
            for item in items:
                txt = item.text()
                self.item_select_name_list.append(txt)
                temp = copy.deepcopy(self.frame_dict[txt])
                self.config_out_list.append(temp)
            self.x.close()


    # 选择的配置项回写
    def f_writeback(self):
        # 先将字典和列表中的原配置项弹出
        frame = self.frame_dict.pop(self.item_select_name)
        index = self.frame_list.index(self.item_select_name)  # 为保证编辑后原有的配置项顺序不变  20170831
        self.frame_list.remove(self.item_select_name)

        # 检查重名问题
        name = self.new.Frame_name.text()
        if self.new.Frame_name.text() in self.frame_dict.keys():
            name += u'__rename'
            i = 1
            while name in self.frame_list:
                name = name[:name.rfind('__rename') + 8] + str(i)
                i += 1
            QMessageBox.information(self.add_but, u"提示", u"已存在同名项，自动更名为:\n")

        # 重新获取配置界面的配置信息
        frame.frame_name = name
        self.item_select_name = frame.frame_name
        self.item_select.setText(frame.frame_name)
        frame.frame_head = self.new.f_head
        # frame.head_chked = self.new.head_chked
        frame.frame_endian = self.new.f_endian
        # frame.tail_chked = self.new.tail_chked
        # frame.frame_trans = self.new.trans
        # frame.trans_chked = self.new.trans_chked
        frame.frame_datCfg_list = self.new.item_list
        frame.frame_datCfg_dict = self.new.item_dict

        # 回写进保存配置的字典和列表
        self.frame_dict[frame.frame_name] = frame
        # self.frame_list.append(unicode(self.item_select.text()))
        self.frame_list.insert(index, self.item_select.text())
        self.item_select = self.listWidget.item(self.listWidget.currentRow())


    # 根据选择的配置项设置子界面
    def UI_Set(self, frame_obj):
        # print unicode(name).encode('utf-8')
        self.new.Frame_name.setText(frame_obj.frame_name)
        self.new.confirm = False  # 20170902添加，消除串帧头的bug
        self.new.Frame_endian.setCurrentIndex(frame_obj.frame_endian)
        # 帧头 相关初始化
        # if frame_obj.head_chked:
        #     self.new.head_check.setCheckState(2)
        self.new.Frame_head.setEnabled(True)
        self.new.Frame_head.setText(frame_obj.frame_head[2:])
        # else:
        #     self.new.head_check.setCheckState(0)
        # self.new.Frame_head.setText("")
        # self.new.Frame_head.setEnabled(False)
        # 帧尾  相关初始化
        # if frame_obj.tail_chked:
        #     self.new.tail_check.setCheckState(2)
        #     self.new.frame_endian.setEnabled(True)
        #     self.new.frame_endian.setText(frame_obj.frame_endian[2:])
        # else:
        #     self.new.tail_check.setCheckState(0)
        #     self.new.frame_endian.setText("")
        #     self.new.frame_endian.setEnabled(False)
        # 转义  相关初始化
        # if frame_obj.trans_chked:
        #     self.new.trans_check.setCheckState(2)
        #     self.new.Frame_trans1.setEnabled(True)
        #     self.new.Frame_trans2.setEnabled(True)
        #     self.new.Frame_trans1.setText(frame_obj.frame_trans[0][2:])
        #     self.new.Frame_trans2.setText(frame_obj.frame_trans[1][2:])
        # else:
        #     self.new.trans_check.setCheckState(0)
        #     self.new.Frame_trans1.setText("")
        #     self.new.Frame_trans2.setText("")
        #     self.new.Frame_trans1.setEnabled(False)
        #     self.new.Frame_trans2.setEnabled(False)

        # 数据域设置  相关初始化
        self.new.item_dict = frame_obj.frame_datCfg_dict
        self.new.item_list = frame_obj.frame_datCfg_list
        row = 0
        self.new.tableWidget.setRowCount(len(frame_obj.frame_datCfg_list))
        # self.choosed.series_No=len(frame_obj.frame_datCfg_list)
        font = QFont()
        font.setPointSize(11)
        for data_set in frame_obj.frame_datCfg_list:
            self.new.tableWidget.setRowHeight(row, 17)

            item = QTableWidgetItem()
            item.setText(str(row + 1))
            item.setFont(font)
            self.new.tableWidget.setItem(row, 0, item)

            item = QTableWidgetItem()
            # print frame_obj.frame_datCfg_dict[data_set].name
            item.setText(frame_obj.frame_datCfg_dict[data_set].name)
            item.setFont(font)
            self.new.tableWidget.setItem(row, 1, item)

            item = QTableWidgetItem()
            style = self.new.sty_dict[frame_obj.frame_datCfg_dict[data_set].dataStyle]
            item.setText(style)

            item.setFont(font)
            self.new.tableWidget.setItem(row, 2, item)

            item = QTableWidgetItem()
            disp = self.new.disp_dict[frame_obj.frame_datCfg_dict[data_set].disp]
            item.setText(disp)
            item.setFont(font)
            self.new.tableWidget.setItem(row, 3, item)

            item = QTableWidgetItem()
            # other = self.new.other_dict[frame_obj.frame_datCfg_dict[data_set].other]
            scal = '%6e' % (frame_obj.frame_datCfg_dict[data_set].scale)
            item.setText(scal)
            item.setFont(font)
            self.new.tableWidget.setItem(row, 4, item)

            row += 1


class frame_style():
    def __init__(self, name):
        self.frame_name = name
        self.frame_head = None
        self.frame_endian = None
        # self.frame_trans = None
        # self.head_chked = False
        # self.tail_chked = False
        # self.trans_chked = False

        self.frame_datCfg_list = []
        self.frame_datCfg_dict = {}


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = QDialog(None)
    x = Ui_Dialog()
    x.setupUi(main)
    main.show()
    sys.exit(app.exec_())
    pass