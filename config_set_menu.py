# -*- coding: utf-8 -*-
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import detect, copy, sys
import config_item_menu
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
        # **** begin 类成员：用于信息获取 ****
        self.confirm = False  # 确认按钮按下后置 True

        self.but_switch = 0  # 1:  add_but clicked
        # 2:  insert_but clicked
        # 3:  edit_but clicked
        # 4:  delete_but clicked

        # 帧格式设置相关
        self.f_head = None
        self.f_endian = 0
        # self.trans = None
        # self.head_chked = False
        # self.tail_chked = False
        # self.trans_chked = False

        # 数据域设置相关
        self.series_No = 1
        self.item_dict = {}
        self.item_list = []
        self.elseInfo = ''
        self.current_item = item_format()
        self.add_count = 1
        self.current_row = 0
        self.sty_dict = {0: 'U_INT 32', 1: 'INT 32', 2: 'Float 32', 3: 'Float 40',
                         4: 'Float 64', 5: 'U_INT 16', 6: 'INT 16', 7: 'U_INT 8', 8: 'INT 8'}

        self.disp_dict = {0: 'DEC显示', 1: 'HEX显示'}
        # self.other_dict={0:'——',1:'位域可解析',2:'值域可解析'}
        # **** end ****

    def setupUi(self, Dialog):
        # Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(813, 578)

        self.config_item = QDialog(Dialog)
        self.config_item_cfg = config_item_menu.Ui_Dialog()
        self.config_item_cfg.setupUi(self.config_item)

        self.tabWidget = QTabWidget(Dialog)
        self.tabWidget.setGeometry(QRect(30, 30, 761, 441))
        font = QFont()
        font.setPointSize(12)
        self.tabWidget.setFont(font)
        # self.tabWidget.setObjectName(_fromUtf8("tabWidget"))

        # **** begin 帧格式设置 相关部件  TAB1 ****
        self.tab = QWidget()
        # self.tab.setObjectName(_fromUtf8("tab"))
        self.label = QLabel(self.tab)
        self.label.setGeometry(QRect(161, 61, 64, 16))
        # self.label.setObjectName(_fromUtf8("label"))
        self.Frame_name = QLineEdit(self.tab)
        self.Frame_name.setGeometry(QRect(231, 61, 167, 22))
        # self.Frame_name.setObjectName(_fromUtf8("Frame_name"))
        self.label_3 = QLabel(self.tab)
        self.label_3.setGeometry(QRect(160, 110, 64, 16))
        # self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_4 = QLabel(self.tab)
        self.label_4.setGeometry(QRect(160, 160, 64, 16))
        # self.label_4.setObjectName(_fromUtf8("label_4"))
        self.Frame_head = QLineEdit(self.tab)
        self.Frame_head.setEnabled(True)
        self.Frame_head.setGeometry(QRect(230, 110, 167, 22))
        # self.Frame_head.setObjectName(_fromUtf8("Frame_head"))
        self.Frame_endian = QComboBox(self.tab)
        self.Frame_endian.addItems(['BigEndian', 'LittleEndian'])
        # self.Frame_endian.setEnabled(False)
        self.Frame_endian.setGeometry(QRect(230, 160, 167, 22))
        # self.Frame_endian.setObjectName(_fromUtf8("Frame_endian"))
        # self.label_5 = QLabel(self.tab)
        # self.label_5.setGeometry(QRect(160, 210, 64, 16))
        # # self.label_5.setObjectName(_fromUtf8("label_5"))
        self.label_6 = QLabel(self.tab)
        self.label_6.setGeometry(QRect(70, 280, 54, 12))
        self.label_6.setText("")
        # self.label_6.setObjectName(u"label_6")
        # self.Frame_trans1 = QLineEdit(self.tab)
        # self.Frame_trans1.setEnabled(False)
        # self.Frame_trans1.setGeometry(QRect(230, 210, 167, 22))
        # self.Frame_trans1.setObjectName(u"Frame_trans1")
        # self.Frame_trans2 = QLineEdit(self.tab)
        # self.Frame_trans2.setEnabled(False)
        # self.Frame_trans2.setGeometry(QRect(433, 210, 167, 22))
        # self.Frame_trans2.setObjectName(u"Frame_trans2")
        # self.head_check = QCheckBox(self.tab)
        # self.head_check.setGeometry(QRect(141, 114, 16, 16))
        # self.head_check.setText("")
        # self.head_check.setVisible(False)
        # self.head_check.setObjectName(_fromUtf8("head_check"))
        # self.tail_check = QCheckBox(self.tab)
        # self.tail_check.setGeometry(QRect(141, 164, 16, 16))
        # self.tail_check.setText("")
        # self.tail_check.setVisible(False)
        # self.tail_check.setObjectName(_fromUtf8("tail_check"))
        # self.trans_check = QCheckBox(self.tab)
        # self.trans_check.setGeometry(QRect(141, 214, 16, 16))
        # self.trans_check.setText("")
        # self.trans_check.setVisible(False)
        # self.trans_check.setObjectName(_fromUtf8("trans_check"))
        # self.label_7 = QLabel(self.tab)
        # self.label_7.setGeometry(QRect(403, 210, 24, 16))
        # self.label_7.setObjectName(_fromUtf8("label_7"))
        self.tabWidget.addTab(self.tab, "")

        # **** end ****

        # **** begin 数据域设置 相关部件  TAB2 ****

        # 表格部件
        self.tab_2 = QWidget()
        # self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.tableWidget = QTableWidget(self.tab_2)
        self.tableWidget.setGeometry(QRect(20, 10, 591, 391))
        # self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setRowCount(0)
        self.tableWidget.verticalHeader().setHidden(True)  # 隐藏行号
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.setShowGrid(False)

        item = QTableWidgetItem()
        item.setTextAlignment(Qt.AlignLeft | Qt.AlignBottom)
        font = QFont()
        font.setPointSize(12)
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QTableWidgetItem()
        item.setTextAlignment(Qt.AlignLeft | Qt.AlignBottom)
        font = QFont()
        font.setPointSize(12)
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QTableWidgetItem()
        item.setTextAlignment(Qt.AlignLeft | Qt.AlignBottom)
        font = QFont()
        font.setPointSize(12)
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QTableWidgetItem()
        item.setTextAlignment(Qt.AlignLeft | Qt.AlignBottom)
        font = QFont()
        font.setPointSize(12)
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QTableWidgetItem()
        item.setTextAlignment(Qt.AlignLeft | Qt.AlignBottom)
        font = QFont()
        font.setPointSize(12)
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(4, item)

        self.tableWidget.setColumnWidth(0, 60)
        self.tableWidget.setColumnWidth(1, 150)
        self.tableWidget.setColumnWidth(2, 110)
        self.tableWidget.setColumnWidth(3, 110)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)

        # 添加按钮
        self.add_but = QPushButton(self.tab_2)
        self.add_but.setGeometry(QRect(640, 50, 81, 31))
        font = QFont()
        font.setPointSize(9)
        self.add_but.setFont(font)
        # self.add_but.setObjectName(_fromUtf8("add_but"))

        # 插入按钮
        self.insert_but = QPushButton(self.tab_2)
        self.insert_but.setGeometry(QRect(640, 100, 81, 31))
        font = QFont()
        font.setPointSize(9)
        self.insert_but.setFont(font)
        # self.insert_but.setObjectName(_fromUtf8("insert_but"))

        # 编辑按钮
        self.edit_but = QPushButton(self.tab_2)
        self.edit_but.setGeometry(QRect(640, 150, 81, 31))
        font = QFont()
        font.setPointSize(9)
        self.edit_but.setFont(font)
        # self.edit_but.setObjectName(_fromUtf8("edit_but"))

        # 删除按钮
        self.del_but = QPushButton(self.tab_2)
        self.del_but.setGeometry(QRect(640, 200, 81, 31))
        font = QFont()
        font.setPointSize(9)
        self.del_but.setFont(font)
        # self.del_but.setObjectName(_fromUtf8("del_but"))

        self.tabWidget.addTab(self.tab_2, "")
        self.line = QFrame(Dialog)
        self.line.setGeometry(QRect(30, 490, 761, 16))
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        # self.line.setObjectName(_fromUtf8("line"))

        # **** end ****

        # **** begin 共用部件 确认和退出按钮 ****
        self.confirm_but = QPushButton(Dialog)
        self.confirm_but.setGeometry(QRect(280, 510, 75, 31))
        # self.confirm_but.setObjectName(_fromUtf8("confirm_but"))
        self.exit_but = QPushButton(Dialog)
        self.exit_but.setGeometry(QRect(400, 510, 75, 31))
        # self.exit_but.setObjectName(_fromUtf8("exit_but"))

        # **** end ****


        # **** begin 各种信号和槽函数 ****

        self.confirm_but.clicked.connect(self.confirm_fun)
        self.exit_but.clicked.connect(Dialog.close)

        # tab1
        # self.head_check.stateChanged.connect(self.head_check_fun)
        # self.tail_check.stateChanged.connect(self.tail_check_fun)
        self.Frame_endian.currentIndexChanged.connect(self.endianSlot)
        # self.trans_check.stateChanged.connect(self.trans_check_fun)

        # tab2
        self.add_but.clicked.connect(self.item_add)
        self.insert_but.clicked.connect(self.item_insert)
        self.edit_but.clicked.connect(self.item_edit)
        self.del_but.clicked.connect(self.item_delete)
        self.tableWidget.itemDoubleClicked.connect(self.item_edit)

        # 其他
        self.config_item.rejected.connect(self.get_itemInfo)


        # **** end ****

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        QMetaObject.connectSlotsByName(Dialog)

        self.x = Dialog

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(u"设置")
        self.label.setText(u"名  称")
        self.label_3.setText(u"帧  头")
        self.label_4.setText(u"字节序")
        # self.label_5.setText(u"转  义")
        # self.label_7.setText(u"-->")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), u"帧格式设置")
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(u"序号")
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(u"名称")
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(u"数据类型")
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(u"显示方式")
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(u"画图比例")

        self.add_but.setText(u"添  加")
        self.add_but.setShortcut(QKeySequence.SelectAll)
        self.add_but.setToolTip(u'Ctrl+A')

        self.insert_but.setText(u"插  入")
        self.insert_but.setShortcut(QKeySequence(u'Ctrl+I'))
        self.insert_but.setToolTip(u'Ctrl+I')

        self.edit_but.setText(u"编  辑")

        self.del_but.setText(u"删  除")
        self.del_but.setShortcut(QKeySequence.Delete)
        self.del_but.setToolTip(u'Delete')

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), u"数据域设置")
        self.confirm_but.setText(u"确  定")
        self.confirm_but.setDefault(True)
        self.exit_but.setText(u"退  出")


    # 槽函数，item设置界面关闭后获取信息
    def get_itemInfo(self):
        if self.config_item_cfg.confirm_flag:  # 必须是通过“确认”按钮退出item设置界面
            self.current_item.name = self.config_item_cfg.it_name
            self.current_item.dataStyle = self.config_item_cfg.it_style
            self.current_item.disp = self.config_item_cfg.it_disp
            # self.current_item.bitSet = self.config_item_cfg.it_bitSet
            self.current_item.scale = self.config_item_cfg.it_scale
            self.add_count = self.config_item_cfg.it_addNum
            # if self.config_item_cfg.it_bitChk:
            #     (self.current_item.bit_chk,self.current_item.num_chk)=(2,0)
            #     self.current_item.other=1  # 位域可解析
            #     pass
            # elif self.config_item_cfg.it_numChk:
            #     (self.current_item.bit_chk,self.current_item.num_chk)=(0,2)
            #     self.current_item.other=2  # 值域可解析
            #     pass
            # else:
            #     (self.current_item.bit_chk,self.current_item.num_chk)=(0,0)
            #     self.current_item.other=0  # ——
            #     pass

            if self.but_switch == 1:  #  按下的是 "添加" 按钮
                self.add_toTab(self.current_item, count=self.add_count)
                self.series_No += self.add_count

            elif self.but_switch == 2:  #  按下的是 "插入" 按钮
                self.add_toTab(self.current_item, count=self.add_count, insert=True)
                self.series_No += self.add_count

            elif self.but_switch == 3:  #  按下的是 "编辑" 按钮
                cur_row = self.tableWidget.currentRow()
                item = self.tableWidget.item(cur_row, 1)
                item.setText(self.current_item.name)
                item = self.tableWidget.item(cur_row, 2)
                item.setText(self.sty_dict[self.current_item.dataStyle])
                item = self.tableWidget.item(cur_row, 3)
                item.setText(self.disp_dict[self.current_item.disp])

                item = self.tableWidget.item(cur_row, 4)
                # if self.config_item_cfg.it_bitChk:
                #     item.setText(_translate("Dialog", self.other_dict[1], None))
                # elif self.config_item_cfg.it_numChk:
                #     item.setText(_translate("Dialog", self.other_dict[2], None))
                # else:
                #     item.setText(_translate("Dialog", self.other_dict[0], None))
                item.setText('%6e' % (self.current_item.scale))

                self.item_list[cur_row] = self.current_item.name
                self.item_dict[self.item_list[cur_row]] = copy.deepcopy(self.current_item)
            else:
                pass
        self.but_switch = 0
        self.config_item_cfg.confirm_flag = False  # 清除config_item_menu界面要使用的重要标志
        self.config_item_cfg.it_add_flag = False

    # 添加数据项到表格中
    def add_toTab(self, current_item, count=1, insert=False):
        font = QFont()
        font.setPointSize(11)
        if insert:
            cur_row = self.tableWidget.currentRow()
            # print cur_row
            for i in range(self.add_count):
                self.tableWidget.insertRow(cur_row)
                # print self.tableWidget.currentRow()
        else:
            # self.series_No=self.tableWidget.currentRow()
            self.tableWidget.setRowCount(self.series_No + count)
            cur_row = self.series_No

        for i in range(self.tableWidget.rowCount()):  # 重新编排“序号”列
            self.tableWidget.setRowHeight(i, 17)
            item = QTableWidgetItem()
            self.tableWidget.setItem(i, 0, item)
            item.setText(str(i + 1))
            item.setFont(font)

        name_tip = u''
        for i in range(count):  # 将新数据项添加进表中
            # 名称
            item = QTableWidgetItem()
            self.tableWidget.setItem(cur_row + i, 1, item)
            if i > 0:
                name_tip = '_' + str(i)
            Qname = current_item.name + name_tip
            item.setText(Qname)
            #name=unicode(Qname,'utf-8','ignore')#.encode('utf-8')
            name = Qname
            item.setFont(font)

            if self.but_switch == 1:
                self.item_list.append(name)  # 添加，使用 append
            elif self.but_switch == 2:
                self.item_list.insert(cur_row + i, name)  # 插入，使用 insert
            self.item_dict[name] = copy.deepcopy(self.current_item)
            self.item_dict[name].name = Qname

            # 数据类型
            item = QTableWidgetItem()
            self.tableWidget.setItem(cur_row + i, 2, item)
            item.setText(self.sty_dict[current_item.dataStyle])
            item.setFont(font)

            # 显示方式
            item = QTableWidgetItem()
            self.tableWidget.setItem(cur_row + i, 3, item)
            item.setText(self.disp_dict[current_item.disp])
            item.setFont(font)

            # 其他
            item = QTableWidgetItem()
            self.tableWidget.setItem(cur_row + i, 4, item)
            # item.setText(_translate("Dialog", self.other_dict[current_item.other], None))
            item.setText('%6e' % (current_item.scale))
            item.setFont(font)

    # def style_check(self,sty):

    # 共用-->   确定
    def confirm_fun(self):
        self.confirm = True
        error = False
        if self.Frame_name.text().strip() == '':
            QMessageBox.warning(self.Frame_head, u"错误", u"名称输入不能为空！")
            error = True
        if not error:
            head = self.Frame_head.text()
            self.f_head = head
            self.f_head = self.f_head.strip()
            if self.f_head.startswith('0x'): self.f_head = self.f_head[2:]
            if self.f_head == '':
                QMessageBox.warning(self.Frame_head, u"错误", u"帧头输入不能为空！")
                error = True
            if len(self.f_head) % 2 > 0:
                QMessageBox.warning(self.Frame_head, u"错误", u"帧头长度应该为整字节数！")
                error = True
            self.f_head = '0x' + self.f_head
            if detect.ishex(self.f_head) == False:
                QMessageBox.warning(self.Frame_head, u"错误", u"请输入合法的16进制帧头！")
                error = True

        if not error:
            self.x.close()

    # 帧格式设置-->   head_check_box 状态
    # def head_check_fun(self):
    #     if self.head_check.checkState() == 2:
    #         self.Frame_head.setEnabled(True)
    #         self.head_chked = True
    #     elif self.head_check.checkState() == 0:
    #         self.Frame_head.setEnabled(False)
    #         self.head_chked = False
    def endianSlot(self):
        self.f_endian = self.Frame_endian.currentIndex()
        # print(self.f_endian)

    # 帧格式设置-->   tail_check_box 状态
    # def tail_check_fun(self):
    #     if self.tail_check.checkState() == 2:
    #         self.Frame_endian.setEnabled(True)
    #         self.tail_chked = True
    #     elif self.tail_check.checkState() == 0:
    #         self.Frame_endian.setEnabled(False)
    #         self.tail_chked = False

    # 帧格式设置-->   trans_check_box 状态
    # def trans_check_fun(self):
    #     if self.trans_check.checkState() == 2:
    #         self.Frame_trans1.setEnabled(True)
    #         self.Frame_trans2.setEnabled(True)
    #         self.trans_chked = True
    #
    #     elif self.trans_check.checkState() == 0:
    #         self.Frame_trans1.setEnabled(False)
    #         self.Frame_trans2.setEnabled(False)
    #         self.trans_chked = False


    # 数据域设置-->  添加
    def item_add(self):
        # self.config_item_cfg.bit_Dialog_cfg.current_bitSet = {}
        self.config_item_cfg.it_name_chkList = self.item_list
        self.config_item_cfg.it_add_flag = True
        self.series_No = self.tableWidget.rowCount()
        # print self.series_No
        self.config_item_dispClear()
        self.but_switch = 1
        self.config_item.show()
        pass

    # 数据域设置-->  插入
    def item_insert(self):
        # self.config_item_cfg.bit_Dialog_cfg.current_bitSet = {}
        self.config_item_cfg.it_add_flag = True
        self.config_item_cfg.it_name_chkList = self.item_list  #  20170904添加  修正在插入时不能检查重名的bug
        self.config_item_dispClear()
        self.but_switch = 2
        self.current_row = self.tableWidget.currentRow()
        self.config_item.show()
        pass

    # 数据域设置-->  编辑
    def item_edit(self):
        self.config_item_dispSet(self.tableWidget.currentRow())
        self.but_switch = 3
        self.config_item.show()
        pass

    # 数据域设置-->  删除   20170827  修改为可以删除多行数据域
    def item_delete(self):
        reply = QMessageBox.information(self.tableWidget, u"提示", u"确认删除？", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            # row = self.tableWidget.currentRow()
            # self.tableWidget.currentItem()
            # QTableWidgetItem.
            row2 = self.tableWidget.selectedItems()
            tmp = [i.row() for i in row2]
            rowindex = list(set(tmp))
            rowindex = sorted(rowindex, reverse=True)  #  从后往前删，可以不用重新排行号  20170830    (用sort排序，修改bug  20170904)
            # print rowindex
            for row in rowindex:
                # row=row2[i]
                # print rowx.row()
                self.tableWidget.removeRow(row)
                self.item_dict.pop(self.item_list[row])
                self.item_list.remove(self.item_list[row])
                self.series_No -= 1
            for i in range(self.tableWidget.rowCount()):  # 重新编排“序号”列
                # self.tableWidget.setRowHeight(i,17)
                item = self.tableWidget.item(i, 0)
                item.setText(str(i + 1))
        pass

    # 针对 config_item 界面显示内容进行设置
    # 设置
    def config_item_dispSet(self, row):
        item = self.item_dict[self.item_list[row]]

        self.config_item_cfg.item_name.setText(item.name)
        self.config_item_cfg.item_style.setCurrentIndex(item.dataStyle)
        self.config_item_cfg.item_disp.setCurrentIndex(item.disp)
        self.config_item_cfg.item_scale.setText(str(item.scale))
        self.config_item_cfg.spinBox.setValue(1)
        self.config_item_cfg.spinBox.setDisabled(True)
        pass

    # 清除
    def config_item_dispClear(self):
        self.config_item_cfg.item_name.clear()
        self.config_item_cfg.item_style.setCurrentIndex(0)
        self.config_item_cfg.item_disp.setCurrentIndex(0)
        self.config_item_cfg.item_scale.setText('1.000000')
        # self.config_item_cfg.bit_check.setCheckState(0)
        # self.config_item_cfg.nums_check.setCheckState(0)
        # self.config_item_cfg.bit_edit_but.setDisabled(True)
        # self.config_item_cfg.nums_edit_but.setDisabled(True)
        self.config_item_cfg.spinBox.setValue(1)
        self.config_item_cfg.spinBox.setDisabled(False)
        pass

    # 清除该界面所有显示
    def UI_Reset(self):
        #  var   reset
        self.confirm = False  # 确认按钮按下后置 True
        self.but_switch = 0

        self.series_No = 1
        self.item_dict = {}
        self.item_list = []
        self.elseInfo = ''
        self.current_item = item_format()
        self.add_count = 1
        self.current_row = 0
        #  tab1  reset
        self.Frame_head.setText('')
        self.Frame_name.setText('')
        self.Frame_endian.setCurrentIndex(0)
        # self.Frame_trans1.setText('')
        # self.Frame_trans2.setText('')
        # self.head_check.setCheckState(2)
        # self.tail_check.setCheckState(0)
        # self.trans_check.setCheckState(0)

        #  tab2  reset
        self.tableWidget.setRowCount(0)


class item_format():
    # def __init__(self,name='',No=0,dataStyle=0,disp=0,bitchk=0,numchk=0,bitset=None,numset=None,other=0):
    def __init__(self, name='', No=0, dataStyle=0, disp=0, scale=1.000000):
        self.name = name
        self.No = No  # 序号
        self.dataStyle = dataStyle
        self.disp = disp
        self.scale = scale
        # self.bit_chk = bitchk
        # self.num_chk = numchk
        # self.bitSet=bitset
        # self.numSet=numset
        # self.other = other # 0: ——   1: 位域可解析   2: 值域可解析


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = QDialog(None)
    x = Ui_Dialog()
    x.setupUi(main)
    main.show()
    sys.exit(app.exec_())
    pass