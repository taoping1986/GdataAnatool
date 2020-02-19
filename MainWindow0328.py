# coding:utf-8

# from Static_Analyze import *
# import Static_Analyze2
# import time
import _thread
# import multiprocessing
import matplotlib
# import qrc_resource
from convert import *
from decimal import Decimal
# matplotlib.use("Qt4Agg")

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys, os, copy, re
import State_Ana
import config_menu, configVal_menu, DataSep
import tablemod
import DataImport

from picture import *
import docset
import sip


# 用于输出重定向  不能删
str3 = []
str4 = ''
i = 0


class MainWindow(QMainWindow):
    stdoutInfo = pyqtSignal(int, name='stdoutMsg')

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.t = 0

        self.choose_Dialog = QDialog(self)
        self.choose_Dialog_set = config_menu.Ui_Dialog()
        self.choose_Dialog_set.setupUi(self.choose_Dialog)

        self.bitcfg_Dialog = QDialog(self)
        # self.bitcfg_Dialog_set=configBit_menu.Ui_Dialog()
        self.bitcfg_Dialog_set = configVal_menu.Ui_Dialog(1)
        self.bitcfg_Dialog_set.setupUi(self.bitcfg_Dialog)

        self.valcfg_Dialog = QDialog(self)
        # self.bitcfg_Dialog_set=configBit_menu.Ui_Dialog()
        self.valcfg_Dialog_set = configVal_menu.Ui_Dialog(2)
        self.valcfg_Dialog_set.setupUi(self.valcfg_Dialog)

        self.dataSep_Dialog = QDialog(self)
        self.dataSep_Dialog_set = DataSep.Ui_Dialog()
        self.dataSep_Dialog_set.setupUi(self.dataSep_Dialog)

        self.setWindowIcon(QIcon("img\\g_data.png"))
        #self.setWindowIcon(QIcon("img\\play.png"))
        self.setWindowTitle("GData AnaTool v3.0")

        # QObject.connect(self, SIGNAL("rejected()"), self.slottest)

        # self.resize(1430,900)               #  界面初始大小设置
        self.resize(800, 600)  #  界面初始大小设置
        self.tab_list = []  #  QWidget 框架
        self.table_list = []  #  QTableView
        self.tab_mod_list = []  #
        self.config_list = []
        self.tabFile_list = []  #  每个页面对应的数据文件路径
        self.tabcfg_list = []
        self.tabFileFmt_list = []  #  每个页面对应数据文件类型： 1-格式化    2-二进制     3-CSV
        self.tabXaxis_list = []  #  每个页面的X轴对应的列，无设置时为-1
        self.tabDispSel_list = []  #  每个页面列的选择，存储checkbox对象组供self.dispDock使用
        self.tabDispChk_list = []  #  列选择的checkbox组的状态
        self.table_index = 0  #   当前数据页的index
        self.table_count = 0  #   数据总页数
        self.binfile_count = 0  #   导入的二进制文件数量的计数器

        self.picData = {}  #   需要画图的列  {table_index:[cols]}
        self.picFlag = False
        self.bitcfg_name = ''
        self.valcfg_name = ''

        self.tabWidget = QTabWidget(self)
        font = QFont()
        font.setPointSize(10)
        self.tabWidget.setFont(font)
        self.tabWidget.setObjectName("tabWidget")
        # QObject.connect(self.tabWidget, SIGNAL("currentChanged(int)"), self.PageChoose)
        self.tabWidget.currentChanged.connect(self.PageChoose)
        self.tabWidget.setTabShape(1)
        self.tabWidget.setTabsClosable(True)

        # self.connect(self.tabWidget,SIGNAL("tabCloseRequested(int)"),self.DPageDel1)
        self.tabWidget.tabCloseRequested.connect(self.DPageDel1)
        # 右键菜单及槽函数设置
        self.createSubMenu()


        # self.textBrowse2=QTextBrowser()
        self.textBrowse = QTextBrowser()
        font = QFont()
        font.setPointSize(12)
        self.textBrowse.setFont(font)
        # self.textEdit=QTextEdit()
        # self.wid=QMessageBox()
        self.setCentralWidget(self.tabWidget)

        self.font = ''
        self.file = ''
        self.findstr = ''
        self.createActions()
        # self.input = QLineEdit()
        # self.input2= QLineEdit()
        self.macro = {}
        self.fun = {}
        self.label = {}
        # self.text = QTextEdit()
        self.createToolBars()
        self.createMenus()
        # self.stdoutInfo=pyqtSignal(int,name='stdoutMsg')
        # self.stdoutMsgSlot=pyqtSlot()
        self.stdoutInfo.connect(self.TextAppend)
        # self.connect(self,SIGNAL('_signal'),self.TextAppend)
        # self.connect(self,SIGNAL('_warn'),self.warn)


        # self.connect(self.choose_Dialog,SIGNAL("rejected()"),self.get_config)
        # self.connect(self.bitcfg_Dialog,SIGNAL("rejected()"),self.get_bitconfig)
        # self.connect(self.valcfg_Dialog,SIGNAL("rejected()"),self.get_valconfig)
        # self.connect(self.dataSep_Dialog,SIGNAL("rejected()"),self.dataSepSlot)

        self.choose_Dialog.rejected.connect(self.get_config)
        self.bitcfg_Dialog.rejected.connect(self.get_bitconfig)
        self.valcfg_Dialog.rejected.connect(self.get_valconfig)
        self.dataSep_Dialog.rejected.connect(self.dataSepSlot)

        # 悬浮窗口1，用于消息打印
        # 新窗口
        self.dock3 = QDockWidget(u"消息", self)
        self.dock3.setFeatures(QDockWidget.AllDockWidgetFeatures)
        wig = QWidget()
        # te3=QTextEdit(self.tr("窗口3,可在Main Window任意位置停靠，可浮动，可关闭"))
        layout = QGridLayout()
        # layout.addWidget(self.inputButton,0,1)
        # layout.addWidget(self.input2,0,0)
        # layout.addWidget(self.text)
        layout.addWidget(self.textBrowse, 0, 0)
        # layout.addWidget(self.textBrowse,0,1)

        wig.setLayout(layout)
        self.dock3.setWidget(wig)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.dock3)
        # Qt.BottomDockWidgetArea
        # self.dock3.close()

        # 悬浮窗口2，用于选择显示的列
        self.dispDock = QDockWidget(u"显示选择", self)
        wig = QWidget(self.dispDock)
        # wig.setSizeIncrement(180,350)
        # wig.setSizePolicy()
        self.listWid = QListWidget(wig)
        # self.listWid.setsize
        self.gridLayout = QGridLayout(wig)
        self.gridLayout.addWidget(self.listWid, 0, 0, 1, 2)
        self.selAll = QCheckBox(wig)
        self.selAll.setCheckState(2)
        self.selAll.setText(u'全选')
        self.gridLayout.addWidget(self.selAll, 1, 0, 1, 1)
        self.selBut = QPushButton(wig)
        self.selBut.setText(u'确定')
        # self.selBut.setFixedSize(70,20)
        self.gridLayout.addWidget(self.selBut, 2, 0, 1, 1)
        self.saveBut = QPushButton(wig)
        self.saveBut.setText(u'保存')
        # self.saveBut.setFixedSize(70,20)
        self.gridLayout.addWidget(self.saveBut, 2, 1, 1, 1)
        wig.setLayout(self.gridLayout)
        self.dispDock.setWidget(wig)
        self.dispDock.setFeatures(QDockWidget.AllDockWidgetFeatures)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dispDock)
        self.dispDock.close()

        # self.connect(self.selBut,SIGNAL("clicked()"),self.selButslot)
        # self.connect(self.saveBut,SIGNAL("clicked()"),self.saveButslot)
        # self.connect(self.selAll,SIGNAL("stateChanged(int)"),self.selAllslot)

        self.selBut.clicked.connect(self.selButslot)
        self.saveBut.clicked.connect(self.saveButslot)
        self.selAll.stateChanged.connect(self.selAllslot)


        # 数据页面选择对话框初始化
        self.lookFlag = False
        self.goflag = 0  # 0: 数据页选择    1: 数据行选择
        self.pageselDia = QDialog(self)
        self.pageselDia.setWindowTitle(u'数据页选择')
        layout = QGridLayout()
        # layout.addWidget(self.text)
        self.golabel = QLabel('Goto Page:')
        # self.pagechoose=QLineEdit(self.pageselDia)
        self.pagechoose = QSpinBox(self.pageselDia)
        layout.addWidget(self.golabel, 0, 0)
        layout.addWidget(self.pagechoose, 0, 1)
        self.buttonBox = QDialogButtonBox(self.pageselDia)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        layout.addWidget(self.buttonBox, 1, 1)
        self.pageselDia.setLayout(layout)
        # QObject.connect(self.buttonBox, SIGNAL("accepted()"), self.showPagex)
        # QObject.connect(self.buttonBox, SIGNAL("rejected()"), self.pageselDia.close)

        self.buttonBox.accepted.connect(self.showPagex)
        self.buttonBox.rejected.connect(self.pageselDia.close)
        # QThread.sleep(3)

        # 20170503  数据文件选择的初始路径
        try:
            pathfile = open('path.txt', 'r')
            path = pathfile.readline()
            # self.fileopenDir = unicode(path ,"utf8")
            self.fileopenDir = path
            # print self.fileopenDir
        except:
            # self.fileopenDir = unicode(os.path.abspath(os.path.curdir))
            self.fileopenDir = os.path.abspath(os.path.curdir)
            # print self.fileopenDir

        # 新增一个数据页面
        self.createDataPage()
        self.pics = []


    # 重写程序退出时的closeEnvent 保存相关信息  20170503
    # 增加删除临时数据文件的操作  20170904
    def closeEvent(self, *args, **kwargs):
        # 保存最后打开数据文件的路径供下次程序运行使用
        f = open('path.txt', 'w')
        f.write(self.fileopenDir)
        f.close()
        # 20170904  添加
        for root, dirs, files in os.walk(r'tempFile'):
            for i in files:
                if i.endswith('.txt'):
                    # print root+os.sep+i
                    os.remove(root + os.sep + i)

    def myContext(self):
        # self.contexMenu.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.contexMenu.exec_(QCursor.pos())
        # self.contexMenu.exec_()
        # self.contexMenu.show()
        pass

    def menu_setX(self):
        # pos=QCursor.pos()
        self.table_index = self.tabWidget.currentIndex()
        item = self.table_list[self.table_index].currentIndex()
        self.tabXaxis_list[self.table_index] = item.column()
        print('>> 设置X轴为第 %d 列。  ' % (item.column() + 1))

    def menu_RowDelete(self):
        reply = QMessageBox.information(self, u"提示", u"删除后无法恢复，确认删除？", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.table_index = self.tabWidget.currentIndex()
            if self.selColumn.isChecked():
                item = self.table_list[self.table_index].currentIndex()
                rowindex = [item.row()]
            else:
                tmp = [i.row() for i in self.table_list[self.table_index].selectedIndexes()]
                rowindex = list(set(tmp))
            rowindex = [delR + self.tab_mod_list[self.table_index].pageindex * 4000 for delR in rowindex]
            # print(rowindex)
            with open(self.tabFile_list[self.table_index], 'r') as f:
                allline = f.readlines()
            with open(self.tabFile_list[self.table_index], 'w') as f:
                for i in range(len(allline)):
                    if i in rowindex:
                        self.table_list[self.table_index].hideRow(i)
                        continue
                    else:
                        f.write(allline[i])
            self.tab_mod_list[self.table_index].updateModel(len(rowindex))
            with open(self.tabFile_list[self.table_index]) as f:
                nowpage = self.tab_mod_list[self.table_index].pageindex
                tmp = nowpage * 4000
                cotent = f.readlines()[tmp:tmp + 4000]
                my_array2 = []
                self.table_list[self.table_index].setModel(QStandardItemModel(self))
                for line in cotent:
                    my_array2.append(line.split())
                # self.tab_mod_list[self.table_index].setUpdatesEnabled(False)
                self.tab_mod_list[self.table_index].arraydata = my_array2[:]
                self.table_list[self.table_index].setModel(self.tab_mod_list[self.table_index])
                # self.table_list[self.table_index].hideRow(item.row())
                # self.contexMenu.

    def H_head_set(self, i, name='', index=0):
        self.item = QStandardItem(name)
        self.tab_mod_list[index].setHorizontalHeaderItem(i, self.item)


    def createDataPage(self):  # 新增一个数据页面，并做相关初始化
        self.tab_list.append(QWidget(self))
        self.table_list.append(QTableView(self.tab_list[self.table_count]))
        self.tab_mod_list.append(QStandardItemModel(self))
        self.table_list[self.table_count].setModel(self.tab_mod_list[self.table_count])
        self.tab_mod_list[self.table_count].setColumnCount(14)

        self.table_list[self.table_count].verticalHeader().setHidden(True)  # 隐藏行号
        self.table_list[self.table_count].verticalHeader().setDefaultSectionSize(17)  # 行高设置为17
        self.table_list[self.table_count].setEditTriggers(QAbstractItemView.NoEditTriggers)  # 不可编辑
        if self.selColumn.isChecked():
            self.table_list[self.table_count].setSelectionBehavior(QAbstractItemView.SelectColumns)  # 选中整行
        else:
            self.table_list[self.table_count].setSelectionBehavior(QAbstractItemView.SelectRows)  # 选中整行
        self.table_list[self.table_count].setContextMenuPolicy(Qt.CustomContextMenu)  # 必须设置，才能使用右键菜单

        # QObject.connect(self.table_list[self.table_count], SIGNAL("customContextMenuRequested(QPoint)"), self.myContext)
        self.table_list[self.table_count].customContextMenuRequested.connect(self.myContext)

        self.tabWidget.addTab(self.tab_list[self.table_count], "Data" + str(self.table_count + 1))

        layout = QGridLayout()
        layout.addWidget(self.table_list[self.table_count], 0, 0)
        self.tab_list[self.table_count].setLayout(layout)

        self.table_count += 1

        # self.tabWidget.setCurrentIndex()
        self.config_list.append([0, 0])
        self.tabFile_list.append('')
        self.tabcfg_list.append('')
        self.tabFileFmt_list.append(0)
        self.tabXaxis_list.append(-1)
        self.tabDispSel_list.append([])
        self.tabDispChk_list.append([])

        count = self.tabWidget.count()
        self.tabWidget.setCurrentIndex(count - 1)

    # 右键菜单及槽函数设置
    def createSubMenu(self):
        self.contexMenu = QMenu(self)
        self.setX = self.contexMenu.addAction(u'该列设为X轴')
        self.setX.triggered.connect(self.menu_setX)
        self.RowDelete = self.contexMenu.addAction(u'删除选中行')
        self.RowDelete.triggered.connect(self.menu_RowDelete)
        # self.RowDelete.setShortcut("Ctrl+L")
        self.ana_menu = self.contexMenu.addMenu(u'分析')
        self.bit_ana = self.ana_menu.addAction(u'位域分析')
        self.bit_ana.triggered.connect(self.menu_bit_Ana)
        self.bit_ana.setEnabled(False)
        self.value_ana = self.ana_menu.addAction(u'值域分析')
        self.value_ana.triggered.connect(self.menu_val_Ana)
        self.value_ana.setEnabled(False)
        # self.draw_menu = self.contexMenu.addMenu(u'画图')
        # self.draw_OneD=QAction(u'一维作图')
        # self.draw_OneD.setShortcut(QKeySequence("Ctrl+1"))
        # self.draw_OneD.triggered.connect(self.addCanvas1D)
        self.draw_OneD = self.contexMenu.addAction(u'一维作图', self.addCanvas1D)

        # self.draw_menu.addAction(self.draw_OneD1)
        # self.draw_OneD.triggered.connect(self.addCanvas1D)
        # self.draw_OneD.triggered.connect(self.draw1D)

        # self.draw_OneD.setShortcut("F11")
        self.draw_TwoD = self.contexMenu.addAction(u'二维作图', self.addCanvas2D)
        # self.draw_TwoD = self.draw_menu.addAction(u'二维作图',self.addCanvas2D,QKeySequence("Ctrl+y"))
        # self.draw_TwoD.triggered.connect(self.addCanvas2D)
        # self.draw_TwoD.setShortcut("F12")

    def createActions(self):
        self.fileOpenAction1 = QAction(QIcon("img\\txt.png"), u"格式化文件", self)
        # self.fileOpenAction.setShortcut("Ctrl+O")
        # self.connect(self.fileOpenAction1,SIGNAL("triggered()"),self.slotOpenFile1)
        self.fileOpenAction1.triggered.connect(self.slotOpenFile1)

        self.fileOpenAction2 = QAction(QIcon("img\\bin.png"), u"二进制文件", self)
        # self.fileOpenAction.setShortcut("Ctrl+O")
        # self.connect(self.fileOpenAction2,SIGNAL("triggered()"),self.slotOpenFile2)
        self.fileOpenAction2.triggered.connect(self.slotOpenFile2)

        # self.fileOpenAction3=QAction(QIcon(":/fileopen.png"),self.tr("CSV文件"),self)
        # self.fileOpenAction.setShortcut("Ctrl+O")
        # self.connect(self.fileOpenAction3,SIGNAL("triggered()"),self.slotOpenFile3)


        self.runAction = QAction(QIcon("img\\play.png"), u"加载", self)
        # self.runAction.setShortcut("Ctrl+N")

        # self.connect(self.runAction,SIGNAL("triggered()"),self.loadFile_thread)
        # self.connect(self.runAction,SIGNAL("triggered()"),self.loadFile)
        # self.connect(self.runAction,SIGNAL("triggered()"),self.loadBFile)
        self.runAction.triggered.connect(self.loadData)
        self.runAction.setDisabled(True)

        # self.fileSaveAction=QAction(QIcon(":/filesave.png"),self.tr("保存"),self)
        # self.fileSaveAction.setShortcut("Ctrl+S")
        # self.fileSaveAction.setStatusTip(self.tr("保存文件"))
        # self.connect(self.fileSaveAction,SIGNAL("triggered()"),self.slotSaveFile)

        self.exitAction = QAction(QIcon("img\\exit.png"), u"退出", self)
        # self.exitAction.setShortcut("Ctrl+Q")
        self.setStatusTip(u"退出")
        self.exitAction.triggered.connect(self.close)

        self.addData = QAction(QIcon("img\\add_data.png"), u"添加数据页", self)
        # self.clsAction=QAction(self.tr("清屏"),self)
        self.addData.setShortcut("Ctrl+A")
        self.addData.triggered.connect(self.DPageAdd)

        self.delData = QAction(QIcon("img\\delete_data.png"), u"删除数据页", self)
        # self.findAction=QAction(self.tr("查找"),self)
        self.delData.setShortcut("Ctrl+D")
        self.delData.triggered.connect(self.DPageDel2)

        self.clsScr = QAction(QIcon(":/eraser.png"), u"清除消息", self)
        # self.findAction=QAction(self.tr("查找"),self)
        # self.clsScr.setShortcut("Ctrl+D")
        self.clsScr.triggered.connect(self.clearScreen)

        self.fontAction = QAction(QIcon(":/font.png"), u"字体", self)
        # self.findAction=QAction(self.tr("查找"),self)
        self.fontAction.setShortcut("F3")
        self.fontAction.triggered.connect(self.fontset)

        # self.reportAction=QAction(QIcon(":/report.png"),self.tr("静态分析"),self)
        self.hextofloatAction = QAction(u"16进制转浮点", self)
        # self.findAction=QAction(self.tr("查找"),self)
        # self.reportAction.setShortcut("F5")
        self.hextofloatAction.triggered.connect(self.hextofloatslot)
        # self.reportAction.setDisabled(True)

        # self.linecountAction=QAction(QIcon(":/linecount.png"),self.tr("代码行统计"),self)
        self.floattohextAction = QAction(u"浮点转16进制", self)
        # self.findAction=QAction(self.tr("查找"),self)
        # self.linecountAction.setShortcut("F6")
        self.floattohextAction.triggered.connect(self.floattohexslot)
        # self.linecountAction.setDisabled(True)

        self.dataSeparateAction = QAction(u'分时复用数据解析', self)
        self.dataSeparateAction.triggered.connect(self.dataSep_Dialog.show)

        self.data1553SepAction = QAction(u'1553B数据分离', self)
        self.data1553SepAction.triggered.connect(self.data1553slot)
        # self.memuseAction=QAction(QIcon(":/mem.png"),self.tr("存储余量"),self)
        # self.findAction=QAction(self.tr("查找"),self)
        # self.memuseAction.setShortcut("F7")
        # self.connect(self.memuseAction,SIGNAL("triggered()"),self.memcount)
        # self.memuseAction.setDisabled(True)

        self.dataitemCfg = QAction(u"数据帧配置", self)
        # self.connect(self.aboutAction,SIGNAL("triggered()"),self.slotAbout)
        self.dataitemCfg.triggered.connect(self.choose_Dialog.show)

        self.bitCfg = QAction(u"位域配置", self)
        # self.connect(self.aboutAction,SIGNAL("triggered()"),self.slotAbout)
        self.bitCfg.triggered.connect(self.bitcfg_Dialog.show)

        self.valCfg = QAction(u"值域配置", self)
        # self.connect(self.aboutAction,SIGNAL("triggered()"),self.slotAbout)
        self.valCfg.triggered.connect(self.valcfg_Dialog.show)

        self.loadAction = QAction(u"导入", self)
        # self.connect(self.aboutAction,SIGNAL("triggered()"),self.slotAbout)
        # self.connect(self.loadAction,SIGNAL("triggered()"),self.choose_Dialog.show)
        self.loadAction.triggered.connect(self.loadActionSlot)

        self.helpAction = QAction(u"使用说明", self)
        self.helpAction.triggered.connect(self.helpActionSlot)

        self.aboutAction = QAction(u"About", self)
        self.aboutAction.triggered.connect(self.aboutActionSlot)

    def loadActionSlot(self):
        file = QFileDialog.getOpenFileName(filter='*.docx;;*.doc')
        file = file[0]
        # file = unicode(QString(file).toUtf8(), 'utf-8', 'ignore')
        if not os.path.isfile(file):
            return
        # self.tabFile_list[self.table_index]=file
        (flag, loadFrame) = docset.testfun(file)
        if flag == -1:
            QMessageBox.information(self, u"错误", self.tr("格式导入文件错误！\n第" + str(loadFrame) + "行"))
            return
        self.choose_Dialog.show()
        self.choose_Dialog_set.UI_Set(loadFrame)
        self.choose_Dialog_set.but_switch = 1  # 类似触发了添加按钮
        self.choose_Dialog_set.new_config.show()

    def helpActionSlot(self):
        # file='usermanual.docx'
        QMessageBox.information(self, u"提示", self.tr("使用说明见本软件目录下的“操作手册.docx”"))
        # x=os.system(file)
        # print x

    def aboutActionSlot(self):
        QMessageBox.information(self, u"关于", self.tr(
            "%s\n\n%s数据解析及可视化工具%s\n\n%sGData V3.0%s\n\n\n\n十七所软件评测中心\n陶平\nTel:  010-63301591\nEmail:  taoping1986@126.com\n%s" %
            (50 * '*', 15 * ' ', 15 * ' ', 20 * ' ', 20 * ' ', 50 * "*")))

    def createMenus(self):  # 20170912  修改菜单各项的文字字体大小为10
        self.fileMenu = QMenu(u'文件')
        font = QFont()
        font.setPointSize(10)  # 20170912
        self.fileMenu.setFont(font)  # 20170912
        # self.fileMenu.setFixedSize()
        self.menuBar().setFont(font)  # 20170912
        # self.fileMenu.setStyleSheet("color: rgb(220, 2, 2);")
        self.menuBar().addMenu(self.fileMenu)
        select = self.fileMenu.addMenu(u'打开')
        select.addAction(self.fileOpenAction1)
        select.addAction(self.fileOpenAction2)
        # select.addAction(self.fileOpenAction3)
        self.recent = self.fileMenu.addMenu(u'最近 ...')
        # with open('recentfile.txt') as f:
        # recent.insertItem(self.tr('测试'))
        linelist = open('recentfile.txt').readlines()
        print(len(linelist))
        try:
            for line in linelist:
                x = line.split()
                filerecent = QAction(self.tr(x[0]), self)
                # self.connect(filerecent,SIGNAL("triggered()"),self.slotOpenRecentFile)
                filerecent.triggered.connect(self.slotOpenRecentFile)
                filerecent.setToolTip(self.tr(x[1]))
                self.recent.addAction(filerecent)
        except:
            pass
        # fileMenu.addAction(self.fileOpenAction)
        self.fileMenu.addAction(self.runAction)
        # fileMenu.addAction(self.fileSaveAction)
        self.fileMenu.addAction(self.exitAction)

        optMenu = self.menuBar().addMenu(u"操作")
        optMenu.setFont(font)
        optMenu.addAction(self.addData)
        optMenu.addAction(self.delData)
        optMenu.addAction(self.clsScr)

        result = self.menuBar().addMenu(u"工具箱")
        result.setFont(font)
        result.addAction(self.hextofloatAction)
        result.addAction(self.floattohextAction)
        result.addAction(self.dataSeparateAction)
        result.addAction(self.data1553SepAction)
        # result.addAction(self.memuseAction)

        configMenu = self.menuBar().addMenu(u"设置")
        configMenu.setFont(font)
        configMenu.addAction(self.dataitemCfg)
        configMenu.addAction(self.bitCfg)
        configMenu.addAction(self.valCfg)
        configMenu.addAction(self.loadAction)

        aboutMenu = self.menuBar().addMenu(u"帮助")
        aboutMenu.setFont(font)
        aboutMenu.addAction(self.helpAction)
        aboutMenu.addAction(self.aboutAction)

    def createToolBars(self):
        fileToolBar = self.addToolBar("File")
        fileToolBar.addAction(self.fileOpenAction1)
        fileToolBar.addAction(self.fileOpenAction2)
        fileToolBar.addAction(self.runAction)
        # fileToolBar.addAction(self.fileSaveAction)
        fileToolBar.addAction(self.exitAction)

        fileToolBar2 = self.addToolBar("Set")
        self.nextpage = QAction(QIcon("img\\NEXT_32PX.png"), u"NextPage", self)
        self.nextpage.triggered.connect(self.shownext)
        self.prevpage = QAction(QIcon("img\\BACK_32PX.png"), u"PrevPage", self)
        self.prevpage.triggered.connect(self.showprev)

        self.gotopage = QAction(QIcon("img\\gopage.png"), u"GoPage", self)
        self.gotopage.setShortcut("Ctrl+P")
        self.gotopage.triggered.connect(self.gopage)

        # 20170615  增加行跳转
        self.gotoline = QAction(QIcon("img\\goto.png"), u"GoLine", self)
        self.gotoline.setShortcut("Ctrl+G")
        self.gotoline.triggered.connect(self.goline)

        self.lookfor = QAction(QIcon("img\\look.png"), u"Find", self)
        self.lookfor.setShortcut("Ctrl+F")
        self.lookfor.triggered.connect(self.lookforSlot)

        self.selColumn = QAction(QIcon("img\\Column.png"), u"RowOrCol", self)
        self.selColumn.triggered.connect(self.ColumnSelect)
        self.selColumn.setCheckable(True)
        self.dispset = QAction(QIcon("img\\choose.png"), u"ColSelect", self)
        self.dispset.setCheckable(True)

        # self.connect(self.dispset,SIGNAL("pressed()"),self.dispFun)
        # self.connect(self.dispset,SIGNAL("released()"),self.undispFun)
        self.dispset.triggered.connect(self.dispFun)
        # fileToolBar2.addAction(self.fontAction)
        fileToolBar2.addAction(self.prevpage)
        fileToolBar2.addAction(self.nextpage)
        fileToolBar2.addAction(self.gotopage)
        fileToolBar2.addAction(self.gotoline)
        fileToolBar2.addAction(self.lookfor)
        fileToolBar2.addAction(self.dispset)
        fileToolBar2.addAction(self.selColumn)

        fileToolBar3 = self.addToolBar("Action")
        self.pic = QAction(QIcon("img\\picture.png"), u"Draw", self)
        self.pic.triggered.connect(self.draw)
        self.closePic = QAction(QIcon("img\\ClosePic.png"), u"ClearPics", self)
        self.closePic.triggered.connect(self.closePicslot)
        # fileToolBar3.addAction(self.draw_OneD)
        # fileToolBar3.addAction(self.draw_TwoD)
        fileToolBar3.addAction(self.pic)
        fileToolBar3.addAction(self.closePic)

    def dispFun(self):
        if self.dispset.isChecked():
            self.dispsetFun()
            self.dispDock.show()
        else:
            self.dispDock.close()

    # def undispFun(self):
    #     self.dispDock.close()
    def dispsetFun(self):
        # if type(self.tab_mod_list[self.table_index])==tablemod.MyTableModel:
        # if self.tabDispSel_list[self.table_index]!=[]:
        headlist = []
        flag = -1
        if self.config_list[self.table_index] != [0, 0]:
            # headdict=self.tab_mod_list[self.table_index].headers
            headlist = self.config_list[self.table_index][0]
            flag = 1
        elif type(self.tab_mod_list[self.table_index]) == tablemod.MyTableModel:
            headlist = self.tab_mod_list[self.table_index].headers.keys()
            flag = 2
            headlist = list(headlist)
            headlist.sort()
        else:
            self.listWid.clear()
            return
        # print flag
        self.listWid.clear()
        # print self.tabDispSel_list[self.table_index]
        # for ind in range(len(headdict.keys())):
        self.tabDispSel_list[self.table_index] = []
        for x in range(len(headlist)):
            item = QListWidgetItem()
            item.setSizeHint(QSize(40, 20))
            checkbox = QCheckBox()
            checkbox.setCheckState(2)
            # checkbox.checkState()
            font = QFont()
            font.setPointSize(12)
            checkbox.setFont(font)
            if flag == 1:
                checkbox.setText('%-6s%-s' % (str(x + 1), headlist[x]))
            else:
                checkbox.setText('%-6s' % (str(x + 1)))
            self.tabDispSel_list[self.table_index].append(checkbox)
            self.listWid.addItem(item)
            self.listWid.setItemWidget(item, checkbox)
        for i in range(len(self.tabDispChk_list[self.table_index])):
            val = self.tabDispChk_list[self.table_index][i]
            self.tabDispSel_list[self.table_index][i].setCheckState(val)

    def shownext(self):
        # self.table_list[self.table_index].hideColumn(2)
        # QTableWidget.hideColumn()
        # print self.t
        if type(self.tab_mod_list[self.table_index]) == tablemod.MyTableModel:
            if self.tab_mod_list[self.table_index].pageindex < self.tab_mod_list[self.table_index].pagecnt - 1:
                self.tab_mod_list[self.table_index].pageindex += 1
                curpage = self.tab_mod_list[self.table_index].pageindex
                tmp = curpage * 4000
                file = self.tabFile_list[self.table_index]
                # t1=datetime.datetime.now()
                # print curpage
                f = open(file)
                if curpage != self.tab_mod_list[self.table_index].pagecnt - 1:
                    cotent = f.readlines()[tmp:tmp + 4000]
                else:
                    cotent = f.readlines()[tmp:]
                f.close()
                my_array2 = []
                self.table_list[self.table_index].setModel(QStandardItemModel(self))
                for line in cotent:
                    my_array2.append(line.split())
                # self.tab_mod_list[self.table_index].setUpdatesEnabled(False)
                self.tab_mod_list[self.table_index].arraydata = my_array2[:]
                self.table_list[self.table_index].setModel(self.tab_mod_list[self.table_index])
                # print type(self.tab_mod_list[self.table_index]),type(tablemod.MyTableModel)
                del my_array2
                gc.collect()
        self.ColHide()
        pass

    def showprev(self):
        if type(self.tab_mod_list[self.table_index]) == tablemod.MyTableModel:
            curpage = self.tab_mod_list[self.table_index].pageindex
            # print 'prev',curpage
            if curpage == 0:
                return
            if curpage <= self.tab_mod_list[self.table_index].pagecnt - 1:
                self.tab_mod_list[self.table_index].pageindex -= 1
                nowpage = self.tab_mod_list[self.table_index].pageindex
                tmp = nowpage * 4000
                file = self.tabFile_list[self.table_index]
                # t1=datetime.datetime.now()
                # print curpage
                f = open(file)
                cotent = f.readlines()[tmp:tmp + 4000]
                f.close()
                my_array2 = []
                self.table_list[self.table_index].setModel(QStandardItemModel(self))
                for line in cotent:
                    my_array2.append(line.split())
                # self.tab_mod_list[self.table_index].setUpdatesEnabled(False)
                self.tab_mod_list[self.table_index].arraydata = my_array2[:]
                self.table_list[self.table_index].setModel(self.tab_mod_list[self.table_index])
                # print type(self.tab_mod_list[self.table_index]),type(tablemod.MyTableModel)
                del my_array2
                gc.collect()
        self.ColHide()
        pass

    def goline(self):
        self.goflag = 1
        self.pageselDia.setWindowTitle(u'数据行跳转')
        # self.golabel.setText('Goto Line:')
        if type(self.tab_mod_list[self.table_index]) == tablemod.MyTableModel:
            self.pagechoose.setMinimum(1)
            max = self.tab_mod_list[self.table_index].linecnt
            self.pagechoose.setMaximum(max)
        else:
            max = 0
            self.pagechoose.setMaximum(0)
        x = 'Goto Line:(1-%d)' % (max)
        self.golabel.setText(x)
        self.pageselDia.show()
        pass

    def gopage(self):
        self.goflag = 0
        self.pageselDia.setWindowTitle(u'数据页跳转')
        self.golabel.setText('Goto Page:')
        if type(self.tab_mod_list[self.table_index]) == tablemod.MyTableModel:
            self.pagechoose.setMinimum(1)
            self.pagechoose.setMaximum(self.tab_mod_list[self.table_index].pagecnt)
        else:
            self.pagechoose.setMaximum(0)
        self.pageselDia.show()
        pass

    def lookforSlot(self):
        self.lookFlag = False
        self.looktoline = 0
        localFlag = False
        v, ok = QInputDialog.getText(self, u"查找值",
                                     u"请输入:",
                                     QLineEdit.Normal, '')
        # n = unicode(QString(v).toUtf8(), 'utf-8', 'ignore')
        n = v
        try:
            if n != u'':
                value = eval(n)
            else:
                return
        except:
            QMessageBox.warning(self, u"警告", u"输入非法！")
            self.lookforSlot()
            return
        if self.selColumn.isChecked():
            self.selColumn.setChecked(False)
            for i in self.table_list:
                i.setSelectionBehavior(QAbstractItemView.SelectRows)  # 选中整行
        if ok:
            if type(self.tab_mod_list[self.table_index]) == tablemod.MyTableModel:
                self.table_index = self.tabWidget.currentIndex()
                item = self.table_list[self.table_index].currentIndex()
                col = item.column()
                row = item.row()
                # print col,row,value
                srcfile = self.tabFile_list[self.table_index]
                array = np.loadtxt(srcfile, dtype=float, usecols=col)
                start = self.tab_mod_list[self.table_index].pageindex * 4000 + row
                for i in range(start, len(array) - 1):
                    if array[i] >= value and array[i + 1] <= value:
                        localFlag = True
                        break
                    elif array[i + 1] >= value and array[i] <= value:
                        localFlag = True
                        break
                if localFlag:
                    self.lookFlag = True
                    self.looktoline = i + 1
                    self.showPagex()
                else:
                    QMessageBox.warning(self, u"信息", u"未找到适配行！")
                pass
            pass

    def showPagex(self):
        if type(self.tab_mod_list[self.table_index]) == tablemod.MyTableModel:
            if self.lookFlag == True:
                x = self.looktoline
                self.goflag = 1
                self.lookFlag = False
            else:
                x = self.pagechoose.value()
            if self.goflag == 0:
                self.tab_mod_list[self.table_index].pageindex = x - 1
                nowpage = self.tab_mod_list[self.table_index].pageindex
            else:
                self.tab_mod_list[self.table_index].pageindex = int((x - 1) / 4000)
                nowpage = self.tab_mod_list[self.table_index].pageindex
            tmp = nowpage * 4000
            file = self.tabFile_list[self.table_index]
            # t1=datetime.datetime.now()
            # print curpage
            f = open(file)
            cotent = f.readlines()[tmp:tmp + 4000]
            f.close()
            my_array2 = []
            self.table_list[self.table_index].setModel(QStandardItemModel(self))
            for line in cotent:
                my_array2.append(line.split())
            # self.tab_mod_list[self.table_index].setUpdatesEnabled(False)
            self.tab_mod_list[self.table_index].arraydata = my_array2[:]
            self.table_list[self.table_index].setModel(self.tab_mod_list[self.table_index])
            if self.goflag == 1:
                if self.selColumn.isChecked():
                    self.selColumn.setChecked(False)
                    for i in self.table_list:
                        i.setSelectionBehavior(QAbstractItemView.SelectRows)  # 选中整行
                self.table_list[self.table_index].selectRow((x - 1) % 4000)
                self.table_list[self.table_index].rowViewportPosition(500)
            # print type(self.tab_mod_list[self.table_index]),type(tablemod.MyTableModel)
            del my_array2
            # print 'Current page: '+str(x)
            gc.collect()
            self.ColHide()

        # self.pageselDia.close()
        pass

    def ColumnSelect(self):
        if self.selColumn.isChecked():
            for i in self.table_list:
                i.setSelectionBehavior(QAbstractItemView.SelectColumns)  # 选中整列
        else:
            for i in self.table_list:
                i.setSelectionBehavior(QAbstractItemView.SelectRows)  # 选中整行
        pass

    def selButslot(self):
        self.tabDispChk_list[self.table_index] = []
        if self.tabDispSel_list[self.table_index] == []:
            return
        for item in self.tabDispSel_list[self.table_index]:
            self.tabDispChk_list[self.table_index].append(item.checkState())
        self.ColHide()

    # 保存文件
    def saveButslot(self):
        # self.file=QFileDialog.getOpenFileName()
        file = QFileDialog.getSaveFileName(filter=u'txt Files(*.txt);;csv Files(*.csv)')[0]
        if file == '':
            return
        savecols = []
        csvhead = ''
        if self.tabDispSel_list[self.table_index] == []:
            return
        for item in self.tabDispSel_list[self.table_index]:
            if item.checkState() == 2:
                col = self.tabDispSel_list[self.table_index].index(item)
                savecols.append(col)
                itemtext = item.text() + u','
                csvhead += itemtext.split()[1]
        # csvhead=csvhead.encode('gbk')
        csvhead = csvhead
        # print savecols
        if savecols != []:
            f = file  #
            # print savecols
            # print ">> 正在保存 %s，请等待......" % (f)
            srcfile = self.tabFile_list[self.table_index]
            try:
                savecontent = np.loadtxt(srcfile, dtype=str, usecols=savecols)
            except:
                print('>> 保存失败，请检查数据文件！')
                return
            # f=open(file,'w')
            # filetmp=unicode('file')
            if f.endswith('.txt'):
                np.savetxt(f, savecontent, fmt='%18s')
            elif f.endswith('.csv'):
                np.savetxt(f, savecontent, delimiter=',', fmt='%s', header=csvhead)
            else:
                return
            print('>> %s 保存完毕！' % f)
            # np.savetxt()
        pass

    def ColHide(self):
        # print self.tabDispChk_list[self.table_index]
        if type(self.tab_mod_list[self.table_index]) == tablemod.MyTableModel:
            for i in range(len(self.tabDispChk_list[self.table_index])):
                val = self.tabDispChk_list[self.table_index][i]
                if val == 0:
                    self.table_list[self.table_index].setColumnHidden(i, True)
                elif val == 2:
                    self.table_list[self.table_index].setColumnHidden(i, False)

    def selAllslot(self):
        i = self.selAll.checkState()
        for item in self.tabDispSel_list[self.table_index]:
            item.setCheckState(i)
            # QCheckBox.setCheckState()

    def hextofloatslot(self):
        value, ok = QInputDialog.getText(self, u"16进制转浮点",
                                         u"请输入16进制:",
                                         QLineEdit.Normal)
        if ok:
            # value=unicode(value).decode('utf-8')
            value = value.replace('0x', '')
            value = value.replace(' ', '')
            if len(value) != 8:
                print('>> 输入错误，应该为4字节！')
                return
            else:
                try:
                    x = hextoFloat(value)
                except:
                    print('>> 输入非法！')
                    return
                print('>> %.6e' % x)
            pass

    def floattohexslot(self):
        value, ok = QInputDialog.getText(self, u"浮点转16进制",
                                         u"请输入浮点数:",
                                         QLineEdit.Normal)
        # unicode(QString(v).toUtf8(), 'utf-8', 'ignore')
        if ok:
            # value=unicode(value).decode('utf-8')
            try:
                value = float(eval(value))
            except:
                print('>> 输入错误！')
                return
            # print('>> 0x%s' % string.upper(floattoHex(value)))
            print('>> 0x%s' % floattoHex(value).upper())


    def data1553slot(self):
        value, ok = QInputDialog.getText(self, u"1553B数据分离",
                                         u"请输入需分离的消息ID(例：[17-R-05-00],[17-R-08-21]):        ",
                                         QLineEdit.Normal)
        if ok:
            # value=unicode(value).decode('utf-8')
            MsgID = [i.strip() for i in value.split(',')]
            # print MsgID
            print('>> Input: ', value)
            if len(MsgID) > 15:
                print('>> 输入消息ID数量不能大于15个！！')
                return
            for id in MsgID:
                if not id.startswith('[') or not id.endswith(']'):
                    print('>> 输入ID错误，请检查！')
                    return
            hlist = DataImport.headget(len(MsgID))
            tmp = QFileDialog.getOpenFileName(directory=self.fileopenDir, filter=u'csv Files(*.csv)')
            self.file = tmp[0]
            # file = unicode(QString(self.file).toUtf8(), 'utf-8', 'ignore')#
            file = self.file  #
            if os.path.isfile(file):
                self.fileopenDir = os.path.dirname(file)
                print('>> 开始分析，分析时间可能较长，请耐心等待.....')
                _thread.start_new_thread(DataImport.D1553Separation, (file, MsgID, hlist))
                # DataImport.D1553Separation(file,MsgID,hlist)


                # self.connect(self.dataSeparateAction,SIGNAL("triggered()"),self.dataSep_Dialog.show)
                # QLineEdit.
                # # unicode(QString(v).toUtf8(), 'utf-8', 'ignore')
                # value=unicode(value).decode('utf-8')
                # try:
                #     value = float(eval(value))
                # except:
                #     print '>> 输入错误！'
                #     return
                # print '>> 0x%s' % string.upper(floattoHex(value))

    # def headget(self,length):
    #     head=[]
    #     for i in range(length):
    #         stmp = '0xff%sff' % ((hex(i+1)[2:])*4)
    #         head.append(stmp)
    #     return head
    #     pass
    def get_config(self):
        if self.choose_Dialog_set.confirm_flag == True and self.choose_Dialog_set.multiItems == False:
            self.choose_Dialog_set.confirm_flag = False  # 此处需清除 flag (fix bug 20170313)
            self.frame_cfg = self.choose_Dialog_set.config_out
            self.data_cfg_dict = self.frame_cfg.frame_datCfg_dict
            self.data_cfg_list = self.frame_cfg.frame_datCfg_list
            self.table_index = self.tabWidget.currentIndex()
            self.config_list[self.table_index] = copy.deepcopy([self.data_cfg_list, self.data_cfg_dict])
            # self.setTable(self.data_cfg_list,self.table_index)   # 根据选择的配置设置表头
            self.tabcfg_list[self.table_index] = self.choose_Dialog_set.item_select_name
            # 20171117
            tabName = self.choose_Dialog_set.item_select_name
            idx = self.tabWidget.currentIndex()
            self.tabWidget.setTabText(idx, tabName)

            # self.tabWidget.setTabToolTip(idx,tabName)
            if type(self.tab_mod_list[
                self.table_index]) == tablemod.MyTableModel:  #  已经导入过某配置的数据，则清除掉显示的数据，页面恢复初始的14列状态
                self.tab_mod_list[self.table_index].arraydata = [[]]
                self.tab_mod_list.pop(self.table_index)
                # self.table_list[self.tabel_index].setModel(QStandardItemModel(self))
                self.tab_mod_list.insert(self.table_index, QStandardItemModel(self))
                self.table_list[self.table_index].setModel(self.tab_mod_list[self.table_index])
                self.tab_mod_list[self.table_index].setColumnCount(14)
            self.listWid.clear()  # 清除dispDock的列表
        elif self.choose_Dialog_set.confirm_flag == True and self.choose_Dialog_set.multiItems == True:
            self.choose_Dialog_set.confirm_flag = False
            self.choose_Dialog_set.multiItems = False
            db_file = shelve.open('config', writeback=True)
            db_file['frame_dict'] = self.choose_Dialog_set.frame_dict
            db_file['frame_list'] = self.choose_Dialog_set.frame_list
            db_file.close()
            self.multifileOpen()
        else:
            pass  # 20170903  修改为：在按"退出"按钮或“x”关闭数据帧配置选择界面时，同样将修改过的配置写入数据库。
            # return
        db_file = shelve.open('config', writeback=True)
        db_file['frame_dict'] = self.choose_Dialog_set.frame_dict
        db_file['frame_list'] = self.choose_Dialog_set.frame_list
        db_file.close()

    def multifileOpen(self):
        # print self.choose_Dialog_set.item_select_name_list
        tmp = QFileDialog.getOpenFileName(directory=self.fileopenDir)
        self.file = tmp[0]
        # file = unicode(QString(self.file).toUtf8(), 'utf-8', 'ignore')#
        file = self.file  #
        if not os.path.isfile(file):
            return
        # print '>> 解析多配置文件中，请等待....'
        for ind in range(len(self.choose_Dialog_set.item_select_name_list)):
            # self.tabFile_list.append(file)
            self.DPageAdd()
            self.frame_cfg = self.choose_Dialog_set.config_out_list[ind]
            self.data_cfg_dict = self.frame_cfg.frame_datCfg_dict
            self.data_cfg_list = self.frame_cfg.frame_datCfg_list
            self.table_index = self.tabWidget.currentIndex()
            self.tabFileFmt_list[self.table_index] = 2  # 二进制文件
            self.tabFile_list[self.table_index] = file
            self.config_list[self.table_index] = copy.deepcopy([self.data_cfg_list, self.data_cfg_dict])
            # self.setTable(self.data_cfg_list,self.table_index)   # 根据选择的配置设置表头
            self.tabcfg_list[self.table_index] = self.choose_Dialog_set.item_select_name_list[ind]
            # 20171117
            tabName = self.choose_Dialog_set.item_select_name_list[ind]
            print('>> ' + tabName)
            idx = self.tabWidget.currentIndex()
            self.tabWidget.setTabText(idx, tabName)
            self.loadData()
        print('>> 解析完成！')
        pass

    # 获取位域设置项的名称bitcfg_name，可据此从config中获取详细配置信息
    def get_bitconfig(self):
        if self.bitcfg_Dialog_set.confirm_flag == True:
            self.bitcfg_name = self.bitcfg_Dialog_set.cfg_name
            self.bitcfg_Dialog_set.confirm_flag = False
            print(u'>> 当前位域配置项： ' + self.bitcfg_name)
            self.bit_ana.setEnabled(True)
        else:
            return

    # 获取位域设置项的名称valcfg_name，可据此从config中获取详细配置信息
    def get_valconfig(self):
        if self.valcfg_Dialog_set.confirm_flag == True:
            self.valcfg_name = self.valcfg_Dialog_set.cfg_name
            self.valcfg_Dialog_set.confirm_flag = False
            print(u'>> 当前值域配置项： ' + self.valcfg_name)
            self.value_ana.setEnabled(True)
        else:
            return

    # 20170815  分时复用数据解析
    def dataSepSlot(self):
        if self.dataSep_Dialog_set.confirm:
            self.dataSep_Dialog_set.confirm = False
            lpcnt = self.dataSep_Dialog_set.loopcnt
            xscale = self.dataSep_Dialog_set.xscale
            lpstart = self.dataSep_Dialog_set.lpstart
            lpend = self.dataSep_Dialog_set.lpend
            cols = self.dataSep_Dialog_set.colist
            self.datasep(lpcnt, xscale, lpstart, lpend, cols)
        else:
            return

    def datasep(self, lpcnt, xscale, lpstart, lpend, cols):
        file = self.tabFile_list[self.table_index]
        # print file
        if self.tabXaxis_list[self.table_index] == -1:
            QMessageBox.warning(self.buttonBox, u"错误", u'请先设定时间轴(x轴)！')
            return
        contents = open(file).readlines()
        if lpend >= len(contents):
            QMessageBox.warning(self.buttonBox, u"错误", u'结束行大于数据文件行数！')
            return
        flist = []
        for i in range(lpcnt):
            f = open('tempFile\\sepFiletemp\\temp%d.txt' % i, 'w')
            flist.append(f)
        if (lpstart, lpend) != (0, 0):
            (begin, end) = (lpstart, lpend)
        else:
            (begin, end) = (0, len(contents))
        lastx = '0'
        i = 0
        linecount = (end - begin) + 1
        t_index = self.tabXaxis_list[self.table_index]
        # try:
        while i < linecount:
            # lostcnt=0
            temp = contents[i].split()
            x = temp[t_index]
            # x_value=eval(x)
            # xvalue = x
            # if xscale!=0 and lastx!=0:
            #     if (x_value-lastx-xscale)>xscale/2.0:   # 检测丢帧：本帧时间-上帧时间-时间刻度 > 时间刻度/2
            #         lostcnt = int(round((x_value-lastx)/xscale)) - 1    # 计算丢失的帧数量,需四舍五入，使用round
            #         if (x_value-lastx)%xscale>xscale/2.0:  # 余数大于刻度值一半则多加一帧
            #             lostcnt+=1
            #         f_index = (f_index+lostcnt+1)%lpcnt
            #         i+=1
            strxscale = str(xscale)
            if xscale != 0 and eval(lastx) != 0:
                if (Decimal(x) - Decimal(lastx) - Decimal(strxscale)) > Decimal(strxscale) / Decimal(
                        '2.0'):  # 检测丢帧：本帧时间-上帧时间-时间刻度 > 时间刻度/2
                    # lostcnt = int(round(((Decimal(x)-Decimal(lastx))/Decimal(strxscale)))) - 1    # 计算丢失的帧数量,需四舍五入，使用round
                    lostcnt = int(round((Decimal(x) - Decimal(lastx)) / Decimal(strxscale))) - 1
                    ttt = (Decimal(x) - Decimal(lastx)) % Decimal(strxscale)
                    if ttt > Decimal(strxscale) / Decimal('2.0'):  # 余数大于刻度值一半则多加一帧
                        lostcnt += 1
                    f_index = (f_index + lostcnt + 1) % lpcnt
                    i += 1
                else:
                    f_index = (f_index + 1) % lpcnt
                    i += 1
            else:
                f_index = i % lpcnt
                i += 1
            temp2 = [x]
            for j in cols:
                temp2.append(temp[j])
            flist[f_index].write('    '.join(temp2) + '\n')
            # lastx=x_value
            lastx = x
        # except:
        #     print '>> 发生错误！请检查解析设置是否正确！'
        for f in flist:
            f.close()
        QMessageBox.information(self, u"提示",
                                u'''<font size=4>解析完成，请及时转存分析结果文件!\n分析结果路径：\\tempFile\\sepFiletemp<\\font>''')
        # QMessageBox.warning(self.buttonBox,u"错误",u'输入含有非法字符！\n请检查!')
        print('>> 解析完成！')


    def PageChoose(self):
        self.table_index = self.tabWidget.currentIndex()
        # 20170503 添加 适应数据页跳转对话框的spinbox的最大值转换
        if type(self.tab_mod_list[self.table_index]) == tablemod.MyTableModel:
            self.pagechoose.setMinimum(1)
            self.pagechoose.setMaximum(self.tab_mod_list[self.table_index].pagecnt)
        else:
            self.pagechoose.setMaximum(0)
        if len(self.tabFile_list) > 0:
            file = self.tabFile_list[self.table_index]
            if not os.path.isfile(file):
                self.runAction.setDisabled(True)
            else:
                self.runAction.setDisabled(False)
        self.dispFun()

    def DPageAdd(self):
        self.createDataPage()

    def DPageDel1(self, index):
        self.table_delindex = index
        self.DPageDel(self.table_delindex)

    def DPageDel2(self):
        self.table_delindex = self.table_index
        self.DPageDel(self.table_delindex)

    def DPageDel(self, table_index):
        if self.table_count > 1:
            self.table_count -= 1
            # if type(self.tab_mod_list[self.table_index])==tablemod.MyTableModel:
            self.tab_mod_list[table_index].arraydata = []
            self.tab_list.pop(table_index)
            tabmod = self.tab_mod_list.pop(table_index)
            tab = self.table_list.pop(table_index)
            # 20171121 注释以下3行 解决删除页面后无法再添加数据页面的bug
            # sip.delete(tabmod)
            # sip.delete(tab)
            # gc.collect()
            self.config_list.pop(table_index)
            self.tabcfg_list.pop(table_index)
            self.tabXaxis_list.pop(table_index)
            self.tabDispSel_list.pop(table_index)
            self.tabDispChk_list.pop(table_index)
            try:
                self.tabFileFmt_list.pop(table_index)
            except:
                pass
            self.tabWidget.removeTab(table_index)  #   必须放最后remove，否则self.table_index发生变化
        else:
            # pass
            QMessageBox.information(self, u"提示：", u"至少保留一个数据页面！")

    # def DPageDel(self,table_index):
    #     if self.table_count>1:
    #         self.table_count -=1
    #         # if type(self.tab_mod_list[self.table_index])==tablemod.MyTableModel:
    #         self.tab_mod_list[self.table_index].arraydata=[]
    #         self.tab_list.pop(self.table_index)
    #         tabmod=self.tab_mod_list.pop(self.table_index)
    #         tab=self.table_list.pop(self.table_index)
    #         # 20171121 注释以下3行 解决删除页面后无法再添加数据页面的bug
    #         # sip.delete(tabmod)
    #         # sip.delete(tab)
    #         # gc.collect()
    #         self.config_list.pop(self.table_index)
    #         self.tabcfg_list.pop(self.table_index)
    #         self.tabXaxis_list.pop(self.table_index)
    #         self.tabDispSel_list.pop(self.table_index)
    #         self.tabDispChk_list.pop(self.table_index)
    #         try:
    #             self.tabFileFmt_list.pop(self.table_index)
    #         except:
    #             pass
    #         self.tabWidget.removeTab(self.table_index)    #   必须放最后remove，否则self.table_index发生变化
    #     else:
    #         # pass
    #         QMessageBox.information(self,u"提示：",u"至少保留一个数据页面！")

    def menu_bit_Ana(self):
        print('>> Bit Analyzing........')
        db_file = shelve.open('config')
        if self.bitcfg_name in db_file['BitCfg_list']:
            self.bitset = db_file['BitCfg_dict'][self.bitcfg_name]
        else:
            print('Error: unvalid bit config!')
            return

        if self.tabXaxis_list[self.table_index] != -1:
            x_axis = self.tabXaxis_list[self.table_index]
        else:
            x_axis = None

        self.table_index = self.tabWidget.currentIndex()
        item = self.table_list[self.table_index].currentIndex()
        column = item.column()

        file = self.tabFile_list[self.table_index]
        # print file
        # State_Ana.state_analyze(x_axis,column,file,self.bitset)
        _thread.start_new_thread(State_Ana.state_analyze, (x_axis, column, file, self.bitset))
        return

    def menu_val_Ana(self):
        print('>> Value Analyzing........')
        db_file = shelve.open('config')
        if self.valcfg_name in db_file['ValCfg_list']:
            self.valset = db_file['ValCfg_dict'][self.valcfg_name]
        else:
            print('>> Error: unvalid bit config!')
            return

        if self.tabXaxis_list[self.table_index] != -1:
            x_axis = self.tabXaxis_list[self.table_index]
        else:
            x_axis = None

        self.table_index = self.tabWidget.currentIndex()
        item = self.table_list[self.table_index].currentIndex()
        column = item.column()

        file = self.tabFile_list[self.table_index]
        # print file,type(file)
        State_Ana.value_analyze(x_axis, column, file, self.valset)

        # thread.start_new_thread(State_Ana.value_analyze,(x_axis,column,file,self.valset))
        return


    # def linecount(self):
    #     result = unicode(QString(self.dir+r'\report\linecount.txt').toUtf8(), 'utf-8', 'ignore')
    #     direction = unicode(QString(self.dir).toUtf8(), 'utf-8', 'ignore')
    #
    #
    #     if not os.path.isfile(result):
    #         QMessageBox.warning(self,self.tr("警告"),self.tr("目标文件夹无代码行统计结果(linecount.txt)！"))
    #         return
    #     pass
    #
    #     text = open(self.dir+'\\report\\linecount.txt').read()
    #     te = unicode(text, 'gbk', 'ignore')
    #
    #     self.textBrowse.setText(self.tr(te))

    # def memcount(self):
    #     result = unicode(QString(self.dir+r'\report\memcount.txt').toUtf8(), 'utf-8', 'ignore')
    #     if not os.path.isfile(result):
    #         QMessageBox.warning(self,self.tr("警告"),self.tr("目标文件夹无内存余量统计结果(memcount.txt)！"))
    #         return
    #     pass
    #
    #     text = open(self.dir+'\\report\\memcount.txt').read()
    #     te = unicode(text, 'gbk', 'ignore')
    #
    #     self.textBrowse.setText(self.tr(te))
    #     pass

    def warn(self):
        QMessageBox.warning(self, 'warning', u"请选择正确的文件夹路径！")

    def slotOpenFile1(self):
        self.tabFileFmt_list[self.table_index] = 1
        self.OpenFile()

    def slotOpenFile2(self):
        self.tabFileFmt_list[self.table_index] = 2
        self.OpenFile()

    # def slotOpenFile3(self):
    #     self.tabFileFmt_list[self.table_index]=3
    #     self.OpenFile()

    def slotOpenRecentFile(self):
        x = QObject.sender(self)
        # file = unicode(x.text())
        file = x.text()
        if os.path.exists(file):
            # print unicode(x.text()),unicode(x.toolTip())
            # if unicode(x.toolTip()) == u'1':
            if x.toolTip() == u'1':
                self.tabFileFmt_list[self.table_index] = 1
            # elif unicode(x.toolTip()) == u'2':
            elif x.toolTip() == u'2':
                self.tabFileFmt_list[self.table_index] = 2
            else:
                print('>> Open Error!')
                return
            if os.path.isfile(file):
                self.runAction.setDisabled(False)
                self.tabFile_list[self.table_index] = file
                # 20171117
                tooltip = os.path.basename(file)
                idx = self.tabWidget.currentIndex()
                self.tabWidget.setTabToolTip(idx, tooltip)
        else:
            QMessageBox.warning(self, u"提示", u"无法打开，文件已被删除、移动或更名！")
        pass

    def OpenFile(self):
        # self.dir=QFileDialog.getExistingDirectory(self)
        # self.file=QFileDialog.getOpenFileName(directory=self.fileopenDir)
        tmp = QFileDialog.getOpenFileName(directory=self.fileopenDir)
        self.file = tmp[0]
        # file = unicode(QString(self.file).toUtf8(), 'utf-8', 'ignore')#
        file = self.file  #

        if os.path.isfile(file):
            self.runAction.setDisabled(False)
            self.tabFile_list[self.table_index] = file
            self.fileopenDir = os.path.dirname(file)
            # 20171117
            tooltip = os.path.basename(file)
            idx = self.tabWidget.currentIndex()
            self.tabWidget.setTabToolTip(idx, tooltip)

            # 20170726 添加  将打开的文件放入recentfile.txt中，为了实现菜单中最近打开文件功能
            f = open('recentfile.txt', 'r')
            content = f.readlines()
            for l in content:
                if file in l:
                    return
            if len(content) >= 5:  # 最多保存5条最近打开文件的记录
                linelist = content[:4]
            else:
                linelist = content
            f.close()
            f = open('recentfile.txt', 'w')
            new = '%s  %d\n' % (file, self.tabFileFmt_list[self.table_index])
            f.write(new)
            for l in linelist:
                f.write(l)
            f.close()
            self.refreshRcFile()

    # 更新“最近 ...” 文件菜单
    def refreshRcFile(self):
        self.recent.clear()
        for line in open('recentfile.txt').readlines():
            x = line.split()
            filerecent = QAction(self.tr(x[0]), self)
            filerecent.triggered.connect(self.slotOpenRecentFile)
            filerecent.setToolTip(self.tr(x[1]))
            self.recent.addAction(filerecent)
        pass

    def loadData(self):
        if self.tabFileFmt_list[self.table_index] == 1:
            # tmp = self.checkDataFile()  #  20170814  检查非法数据，仅在导入格式化文本时检查
            # if tmp>=0:
            #     print '>> 数据文件含有非法数据! (Line:%d)' % (tmp)
            #     QMessageBox.warning(self,u"错误",self.tr('数据文件含有非法数据! (Line:%d)' % (tmp)))
            #     return
            self.loadFile()
        elif self.tabFileFmt_list[self.table_index] == 2:
            self.loadBFile()
        # elif self.tabFileFmt_list[self.table_index]==3:
        #     self.loadCsvFile()
        else:
            print(">> Error!(109)")
            return

    # 检查数据文本文件中是否含有非法数据字符[^0-9a-fA-Fx+.\-\s]   20170814
    def checkDataFile(self):
        file = self.tabFile_list[self.table_index]
        with open(file) as f:
            i = 0
            for line in f:
                i += 1
                # if 'nan' in line or '#' in line:
                if re.match('.*[^0-9a-fA-Fx+.\-\s].*', line):
                    # print 'File Error!'
                    return i
        return -1

    def loadFile(self, hexcols=[]):  #  加载一般的格式化文件，空白符分隔的数据
        file = self.tabFile_list[self.table_index]
        # t1=datetime.datetime.now()
        try:
            f = open(file)
        except:
            return
        line1 = f.readline()
        f.seek(0, 0)
        # self.tab_mod.setRowCount(len(content))
        f.close()
        self.table_index = self.tabWidget.currentIndex()
        cnt = len(line1.split())
        cfg = self.config_list[self.table_index][0]
        if cfg != [] and cfg != 0:
            if cnt == 0:  # 20170912  增加格式错误，一帧数据都未解出时的提示
                QMessageBox.warning(self, u"错误", u"<font size=4>未解析出与数据帧配置匹配的数据帧，请检查数据帧配置或重新选择数据文件！<\\font>")
                return
            elif len(cfg) != cnt:
                QMessageBox.warning(self, u"错误", u"所选配置项与数据文件的列数不匹配，请重新选择配置项！")
                return
            else:  # 20170814  检查当前数据文件是否有16进制显示的行，若有则转换为10进制，并获取配置中16进制显示的列hexcols,否则转存为临时文件
                cfgDict = self.config_list[self.table_index][1]
                hexcols = [cfg.index(item) for item in cfg if cfgDict[item].disp != 0]
                # print hexcols
                hexdisp = self.checkDisp(line1)
                # if hexdisp != []:
                self.tabFile_list[self.table_index] = DataImport.DataFileReplace(file, hexdisp)  #替换为处理后数据文件
        else:
            self.tabFile_list[self.table_index] = DataImport.DataFileReplace(file)
            #     print 'Match!'
            # else:
            #     print 'Not match!'
        f = open(self.tabFile_list[self.table_index])
        content = f.readlines()

        my_array2 = []
        for line in content:
            my_array2.append(line.split())
        linecnt = len(my_array2)
        tablemodel = tablemod.MyTableModel(my_array2[:4000], self.config_list[self.table_index][0], linecnt, hexcols,
                                           self)
        self.tab_mod_list[self.table_index] = tablemodel
        self.table_list[self.table_index].setModel(tablemodel)
        self.dispFun()
        self.ColHide()

    def checkDisp(self, line):
        x = line.split()
        res = []
        for i in range(len(x)):
            if 'x' in x[i]:
                res.append(i)
        return res

    def loadBFile(self):  #  加载二进制文件
        self.load_flag = True
        file = self.tabFile_list[self.table_index]
        # print file

        # t1 = datetime.datetime.now()
        # if self.table_index in self.config_list.keys():
        if self.config_list[self.table_index][0] != 0:
            cfg = self.tabcfg_list[self.table_index]  #  传递配置的名称
            cfg_ana = DataImport.CfgProcess(cfg)
            self.binfile_count += 1
            fname = 'tempFile\\bin2txt_tmp' + str(self.binfile_count) + '.txt'
            hexcol = DataImport.ReadBfile(file, cfg_ana, fname)
        # t2 = datetime.datetime.now()
        self.tabFile_list[self.table_index] = fname
        # print t2-t1
        self.loadFile(hexcols=hexcol)
        # t3 = datetime.datetime.now()
        # print t3-t2
        return hexcol

    def loadCsvFile(self):  #  加载csv格式的文件
        pass

    def loadFile_thread(self):
        self.runAction.setDisabled(True)
        _thread.start_new_thread(self.loadFile, ())
        # thread.start_new_thread(self.loadBFile,())

    def draw(self):
        inFile = []
        cfg = []
        AxisX = []
        columnlist = []
        self.picFlag = True
        # print self.picData
        if self.draw_TwoD.isEnabled():
            for index, cols in self.picData.items():
                inFile.append(self.tabFile_list[index])
                cfg.append(self.tabcfg_list[index])
                AxisX.append(self.tabXaxis_list[index])
                columnlist.append(cols)
                # inFile=self.tabFile_list[self.table_index]
                # cfg = self.tabcfg_list[self.table_index]
                # p = multiprocessing.Process(target = drawcanvas, args = (inFile,cfg,AxisX,columnlist,))
                # p.start()
                #if self.draw_TwoD.isEnabled():
            # print inFile,cfg,columnlist
            form = AppForm(inFile, cfg, columnlist, xAxis=AxisX, D1_flag=False)
            form.show()
            self.pics.append(form)
        elif self.draw_OneD.isEnabled():
            for index, cols in self.picData.items():
                inFile.append(self.tabFile_list[index])
                cfg.append(self.tabcfg_list[index])
                # AxisX.append(self.tabXaxis_list[index])
                columnlist.append(cols)
            form = AppForm(inFile, cfg, columnlist, xAxis=None, D1_flag=True)
            form.show()
            self.pics.append(form)
        self.draw_OneD.setEnabled(True)
        self.draw_TwoD.setEnabled(True)
        pass

    def closePicslot(self):
        for form in self.pics:
            form.close()
            form.exitslot()
            sip.delete(form)
            gc.collect()
        del self.pics
        gc.collect()
        self.pics = []
        self.draw_TwoD.setEnabled(True)
        self.draw_OneD.setEnabled(True)

    def slottest(self):
        f = open('toolexit.txt')
        print('slottest')

    # def close(self):
    #     self.closeEvent()
    #     print 'close cz!'
    @pyqtSlot()
    def addCanvas1D(self):
        # print("1d")
        if self.draw_TwoD.isEnabled():
            self.draw_TwoD.setEnabled(False)
            self.picFlag = True
        if self.picFlag == True:
            self.picData.clear()
            self.picFlag = False

        if self.selColumn.isChecked():  # 优化，防止在行选择状态时把所有列都加入画布  0724
            itemlist = self.table_list[self.table_index].selectedIndexes()
            Addlist = []
            for item in itemlist:
                if self.table_index not in self.picData.keys():
                    self.picData[self.table_index] = []
                colnum = item.column()
                Addlist.append(colnum)
                if colnum not in self.picData[self.table_index]:
                    self.picData[self.table_index].append(colnum)
                    # Addlist.append(colnum)
                    # else:
            Addlist = list(set(Addlist))
            if len(Addlist) != 0:
                tmp = []
                for i in Addlist:
                    tmp.append(self.tab_mod_list[self.table_index].headers[i])
                    # tmp.append(item.text())
                # self.selColumn
                print(""">> 添加 "表%s" 中 "%s" 列到一维画布。 """ % (self.tabWidget.tabText(self.table_index), ','.join(tmp)))
        else:
            self.table_index = self.tabWidget.currentIndex()
            item = self.table_list[self.table_index].currentIndex()
            colnum = item.column()
            if colnum >= 0:
                # print colnum
                if self.table_index not in self.picData.keys():
                    self.picData[self.table_index] = []
                if colnum not in self.picData[self.table_index]:
                    self.picData[self.table_index].append(colnum)
                print(""">> 添加 "表%s" 中 "%s" 列到一维画布。 """ % (self.tabWidget.tabText(self.table_index),
                                                           self.tab_mod_list[self.table_index].headers[colnum]))


    def addCanvas2D(self):
        if self.tabXaxis_list[self.table_index] == -1:
            QMessageBox.warning(self, u"提示", u"请先设定X轴！")
            return

        if self.draw_OneD.isEnabled():
            self.draw_OneD.setEnabled(False)
            self.picFlag = True

        # print self.picFlag
        if self.picFlag == True:
            self.picData.clear()
            self.picFlag = False

        if self.selColumn.isChecked():  # 优化，防止在行选择状态时把所有列都加入画布  0724
            itemlist = self.table_list[self.table_index].selectedIndexes()
            Addlist = []
            for item in itemlist:
                if self.table_index not in self.picData.keys():
                    self.picData[self.table_index] = []
                colnum = item.column()
                Addlist.append(colnum)
                if colnum not in self.picData[self.table_index]:
                    self.picData[self.table_index].append(colnum)
            Addlist = list(set(Addlist))
            if len(Addlist) != 0:
                tmp = []
                for i in Addlist:
                    tmp.append(self.tab_mod_list[self.table_index].headers[i])
                    # tmp.append(item.text())
                # self.selColumn
                print(""">> 添加 "表%s" 中 "%s" 列到二维画布。 """ % (self.tabWidget.tabText(self.table_index), ','.join(tmp)))
        else:
            self.table_index = self.tabWidget.currentIndex()
            item = self.table_list[self.table_index].currentIndex()
            colnum = item.column()
            # print colnum
            if colnum >= 0:
                if self.table_index not in self.picData.keys():
                    self.picData[self.table_index] = []
                if colnum not in self.picData[self.table_index]:
                    self.picData[self.table_index].append(colnum)
                print(""">> 添加 "表%s" 中 "%s" 列到一维画布。 """ % (self.tabWidget.tabText(self.table_index),
                                                           self.tab_mod_list[self.table_index].headers[colnum]))

                # print self.picData

    def slotSaveFile(self):
        self.file = QFileDialog.getSaveFileName()
        pass

    def clearScreen(self):
        global str4
        self.textBrowse.clear()
        str4 = ''

    def fontset(self):
        # f,ok=QFontDialog.setsize#getFont()
        size, ok = QInputDialog.getText(self, u"字体大小",
                                        u"请输入:",
                                        QLineEdit.Normal, self.font)
        # n = unicode(QString(size).toUtf8(), 'utf-8', 'ignore')
        n = size
        # print n
        if ok:
            # self.fontLineEdit.setFont(f)
            # text=self.textBrowse.tex
            self.textBrowse.setFont(QFont("Timers", eval(n)))
            # self.textBrowse.setText(text)
            # self.text.setFont(QFont("Timers",eval(n)))

            # self.textBrowse.setFontPointSize(eval(n))
            # pass

    # 输出重定向的write函数
    def write(self, *args, **kwargs):
        global str3, str4
        s = args[0]
        str3.append(s[:])
        str4 += self.tr(s[:])
        # self.emit(SIGNAL('_signal'))
        self.stdoutMsg.emit(1)

    # 槽函数：  输出重定向函数write中的_signal信号触发
    # 功能：    将输出内容显示到文本框中
    def TextAppend(self):
        self.textBrowse.setText(str4)
        self.textBrowse.moveCursor(QTextCursor.End)  # 滚动条指向文本框最末端
        # self.textBrowse2.setText(str4)

        # def drawcanvas(self,inFile,cfg,AxisX,columnlist):
        #     # app = QApplication(sys.argv)
        #     # self.picflag=True
        #     # form = AppForm('test.dat',u'21ca-mid',0,[90,91,92])
        #     self.form = AppForm(inFile,cfg,AxisX,columnlist)
        #     # form.show()
        #     self.picflag=True
        #     # return self.form


# def drawcanvas(inFile,cfg,AxisX,columnlist):
#         app = QApplication(sys.argv)
#
#         # form = AppForm('test.dat',u'21ca-mid',0,[90,91,92])
#         form = AppForm(inFile,cfg,AxisX,columnlist)
#         form.show()
#         # return form
#         app.exec_()

def main():
    # import qtmodern
    app = QApplication([])
    # splash=QSplashScreen(QPixmap("img\\timg.png"))
    # splash.show()
    # app.processEvents()
    main = MainWindow()

    sys.stdout = main
    # main.show()
    main.showMaximized()  #  以最大化显示
    # f=open('logfile.txt','w')
    # f.close()
    app.exec_()


def ui_start(e):
    app = QApplication([])
    splash = QSplashScreen(QPixmap("img\\timg.png"))
    splash.show()
    e.wait()
    splash.close()
    app.exec_()


if __name__ == '__main__':
    # multiprocessing.freeze_support()   # 多进程程序打包，必须添加该语句
    # e = multiprocessing.Event()
    # p1 = multiprocessing.Process(target = ui_start,args = (e,))
    # p2 = multiprocessing.Process(target = main,args = (e,))
    # p1.start()
    # p2.start()
    main()
    # app=QApplication(sys.argv)
    # t1=datetime.datetime.now()
    # main=MainWindow()
    # sys.stdout=main
    # main.show()
    # t2=datetime.datetime.now()
    # main.t=t2-t1
    # app.exec_()
