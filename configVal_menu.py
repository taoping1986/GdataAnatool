# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'config_menu3.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys, os, shelve, copy
import bit_set, val_set

butsty = """{border-radius: 4px;
        border: none;
        width: 75px;
        height: 25px;
        background: rgb(0, 165, 235);
        color: white;}"""

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
    def __init__(self, flag):  # flag=1:  位域   2:值域
        self.but_switch = 0  # 按键检测：1-添加  2-编辑  0-其他
        self.current_config = None
        self.confirm_flag = False
        self.cfg_name = None  # 传递选择的配置项的名称(unicode)
        if flag == 1:
            self.listname = 'BitCfg_list'
            self.dictname = 'BitCfg_dict'
            self.dialogname = "位域分析配置项选择"
            self.new = bit_set.Ui_Dialog()
        else:
            self.listname = 'ValCfg_list'
            self.dictname = 'ValCfg_dict'
            self.dialogname = "值域分析配置项选择"
            self.new = val_set.Ui_Dialog()
        pass

    def setupUi(self, Dialog):
        # Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(341, 478)
        self.x = Dialog

        self.new_config = QDialog(Dialog)  # 配置项编辑的子界面
        self.new.setupUi(self.new_config)

        self.listWidget = QListWidget(Dialog)
        self.listWidget.setGeometry(QRect(10, 20, 201, 401))
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
        self.confirm_but = QPushButton(Dialog)
        self.confirm_but.setGeometry(QRect(240, 340, 75, 31))
        # self.confirm_but.setObjectName(_fromUtf8("confirm_but"))
        self.confirm_but.setDisabled(True)
        self.exit_but = QPushButton(Dialog)
        self.exit_but.setGeometry(QRect(240, 390, 75, 31))
        # self.exit_but.setObjectName(_fromUtf8("exit_but"))

        self.add_but.clicked.connect(self.add_config)
        self.new_config.rejected.connect(self.add_item)  # 添加新的帧格式
        self.edit_but.clicked.connect(self.edit_config)

        self.listWidget.itemSelectionChanged.connect(self.itemSelected)
        self.listWidget.itemDoubleClicked.connect(self.edit_config)

        self.del_but.clicked.connect(self.item_delete)
        self.copy_but.clicked.connect(self.item_saveas)

        self.confirm_but.clicked.connect(self.confirm)
        self.exit_but.clicked.connect(self.exitslot)

        # self.listWidget, SIGNAL(_fromUtf8("itemSelectionChanged()")), self.choosed_func)

        if os.path.exists('config.dat'):
            self.listSet()
        self.retranslateUi(Dialog)
        QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(self.dialogname)
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

        self.confirm_but.setText(u"确 认")
        self.confirm_but.setDefault(True)
        self.exit_but.setText(u"退 出")

    # 添加按钮槽函数
    def add_config(self):
        self.but_switch = 1  # 添加按钮触发
        self.new.UI_Reset()  # 清空界面
        self.new_config.show()

    # 编辑按钮槽函数
    def edit_config(self):
        self.but_switch = 2  # 编辑按钮触发
        name = self.item_select_name
        self.new.UI_Set(name)
        self.new_config.show()

    # 设置界面退出槽函数
    def add_item(self):
        # 添加新配置项
        self.listSet()
        # if self.new.confirm_flag == True and self.but_switch == 1:
        #     name = unicode(self.new.name.text())#.encode('utf-8')
        #     item = QListWidgetItem()
        #     font = QFont()
        #     font.setPointSize(12)
        #     item.setFont(font)
        #     # item.setText(self.new.Frame_name.text())
        #     item.setText(name)
        #     self.listWidget.addItem(item)
        #     self.new.confirm_flag = False
        # # 回写选中的配置项
        # elif self.new.confirm_flag == True and self.but_switch == 2:
        #     self.new.confirm_flag = False
        pass

    # 删除按钮槽函数
    def item_delete(self):
        self.item_select = self.listWidget.item(self.listWidget.currentRow())
        if self.item_select is None:
            QMessageBox.information(self.listWidget, u"提示", u"请先选择需删除的项！")
            return
        reply = QMessageBox.information(self.listWidget, u"提示", u"确认删除？", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            name = self.item_select.text()
            # name = unicode(name)#unicode(name,'utf-8','ignore').encode('utf-8')
            self.listWidget.takeItem(self.listWidget.currentRow())
            db_file = shelve.open('config', writeback=True)
            db_file[self.listname].remove(name)
            db_file[self.dictname].pop(name)
            if len(db_file[self.listname]) == 0:
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
        if self.item_select is None:
            QMessageBox.information(self.listWidget, u"提示", u"请先选择需另存的配置项！")
            return
        name = self.item_select.text()
        # name = unicode(name)
        index = 1
        name_temp = name

        db_file = shelve.open('config', writeback=True)
        while name_temp in db_file[self.listname]:
            name_temp = name + u'复件' + str(index)
            index += 1
            item.setText(name_temp)
        self.listWidget.addItem(item)
        new_item = copy.deepcopy(db_file[self.dictname][name])
        new_name = item.text()

        # db_file=shelve.open('config',writeback=True)
        db_file[self.listname].append(new_name)
        db_file[self.dictname][new_name] = new_item
        db_file.close()


    # 列表选项选择槽函数
    def itemSelected(self):
        self.del_but.setDisabled(False)
        self.edit_but.setDisabled(False)
        self.copy_but.setDisabled(False)
        self.confirm_but.setDisabled(False)
        self.item_select = self.listWidget.item(self.listWidget.currentRow())
        if self.item_select == None:
            self.del_but.setDisabled(True)
            self.edit_but.setDisabled(True)
            self.copy_but.setDisabled(True)
            self.confirm_but.setDisabled(True)
            return
        name = self.item_select.text()
        self.item_select_name = name

    # 确定按钮槽函数
    def confirm(self):
        self.confirm_flag = True
        # self.item_select = self.listWidget.item(self.listWidget.currentRow())
        self.cfg_name = self.item_select_name
        # print self.cfg_name
        self.x.close()

    def exitslot(self):
        self.confirm_flag = False
        self.x.close()


    # 设置列表内容
    def listSet(self):
        ind = self.listWidget.currentIndex()
        self.listWidget.clear()
        db_file = shelve.open('config')
        if self.listname in db_file.keys() and self.dictname in db_file.keys():
            for x in db_file[self.listname]:
                item = QListWidgetItem()
                font = QFont()
                font.setPointSize(12)
                item.setFont(font)
                item.setText(x)
                self.listWidget.addItem(item)
        db_file.close()
        # 重置界面后恢复选定的选项  20170902
        self.listWidget.setCurrentIndex(ind)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # app.setStyleSheet("QPushButton "+butsty)
    main = QDialog(None)
    x = Ui_Dialog(2)
    x.setupUi(main)
    main.show()
    sys.exit(app.exec_())
    pass