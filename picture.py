# -*- coding: utf-8 -*-

import sys
# import numpy as np
import matplotlib
# import qrc_resource
matplotlib.use("Qt4Agg")
# from matplotlib.figure import Figure
# from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
# from matplotlib.backends import qt_compat
from matplotlib import font_manager
# use_pyside = qt_compat.QT_API == qt_compat.QT_API_PYSIDE

# from guppy import hpy  #内存消耗测试
# import gc

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from draw import *
# QTextCodec.setCodecForTr(QTextCodec.codecForName("utf8"))
class AppForm(QWidget):
    # class AppForm(QDialog):
    def __init__(self, inFile, cfg, index, xAxis=None, D1_flag=False, parent=None):
        QWidget.__init__(self, parent)
        try:  # 20170814 通过pic.cfg的第二行，控制点标注的浮点数显示位数
            f = open('pic.cfg')
            x = f.readlines()[-1]
            x = eval(x)
            if x > 10:
                x = 10
            elif x < 2:
                x = 2
            self.annoteLen = '%%.%de' % (x)
        except:
            self.annoteLen = '%.4e'

        if D1_flag == False:  # 画二维图
            self.pic2D(inFile, cfg, xAxis, index)
        elif D1_flag == True:  # 画一维图
            self.pic1D(inFile, cfg, index)
        # self.data = self.get_data2()
        self.create_main_frame()
        # print "Heap at the end of the functionn", hp.heap()
        # self.on_draw()
        # QObject.connect(self, SIGNAL("_signalexit"), self.testslot)

    def create_main_frame(self):
        # self.main_frame = QWidget()
        self.canvas = self.fig.canvas
        self.mpl_toolbar = NavigationToolbar(self.canvas, self, coordinates=False)
        self.mpl_toolbar.addSeparator()
        # self.mpl_toolbar.addAction(self.mpl_toolbar._icon("style.png"),'Customize',self.get_data2)
        self.anoteAction = self.mpl_toolbar.addAction(QIcon("img\\location.png"), 'Point Note', self.anoteset)
        # self.exitAction=self.mpl_toolbar.addAction(QIcon("style.png"),'Point Note',self.exitslot)
        self.anoteAction.setCheckable(True)
        # self.mpl_toolbar.addSeparator()
        # action=self.mpl_toolbar.addAction(self.mpl_toolbar._icon("qt.png"),
        # 'Customize', self.get_data2)
        # action.setCheckable(True)

        # self.canvas.mpl_connect('key_press_event', self.on_key_press)

        # vbox = QVBoxLayout()
        # vbox.addWidget(self.mpl_toolbar)
        # vbox.addWidget(self.canvas)  # the matplotlib canvas
        # self.setLayout(vbox)
        # self.main_frame.setLayout(vbox)
        # self.setCentralWidget(self.main_frame)

        # print self.mpl_toolbar
        self.chklist = []
        self.listwid = QListWidget(self)
        for x in range(len(self.lnamelist)):
            item = QListWidgetItem()
            checkbox = QCheckBox()

            checkbox.setCheckState(2)
            # checkbox.checkState()
            font = QFont()
            font.setPointSize(12)
            checkbox.setFont(font)
            checkbox.setText('   %s' % (self.lnamelist[x]))
            checkbox.stateChanged.connect(self.chklistSlot)
            self.chklist.append(checkbox)
            self.listwid.addItem(item)
            self.listwid.setItemWidget(item, checkbox)

        gridLayout = QGridLayout()
        # gridLayout.addWidget(self.mpl_toolbar,0,0,1,4)
        # gridLayout.addWidget(self.canvas,1,0,3,3)
        # gridLayout.addWidget(self.listwid,1,3,3,1)
        gridLayout.addWidget(self.mpl_toolbar, 0, 0)
        gridLayout.addWidget(self.canvas, 1, 0)
        gridLayout.addWidget(self.listwid, 1, 1)
        gridLayout.setColumnStretch(0, 2)
        gridLayout.setColumnStretch(0, 1)
        self.setLayout(gridLayout)
        # self.dispDock=QDockWidget(self.tr("显示选择"),self)
        # wig=QWidget(self.dispDock)
        #
        # wig.setSizeIncrement(180,350)
        # self.listWid = QListWidget(wig)
        # self.gridLayout=QGridLayout(wig)
        # self.gridLayout.addWidget(self.listWid, 0, 0, 1, 2)
        # wig.setLayout(self.gridLayout)
        # self.dispDock.setWidget(wig)
        # self.dispDock.setFeatures(QDockWidget.AllDockWidgetFeatures)
        # self.addDockWidget(Qt.RightDockWidgetArea,self.dispDock)

    def get_data2(self):
        # print 'asda'
        return np.arange(20).reshape([4, 5]).copy()

    def on_draw(self):
        self.canvas.draw()
        # plt.show()

    def on_key_press(self, event):
        print('you pressed', event.key)
        # implement the default mpl key press events described at
        # http://matplotlib.org/users/navigation_toolbar.html#navigation-keyboard-shortcuts
        # key_press_handler(event, self.canvas, self.mpl_toolbar)

    def pic1D(self, inFilelist, cfglist, colslist):
        self.fig, self.ax = plt.subplots(1, 1)
        self.datalist = []
        self.linelist = []
        self.lnamelist = []
        self.fmtlist = []
        zh_font = font_manager.FontProperties(fname=r'c:\windows\fonts\simsun.ttc', size=10)
        if len(inFilelist) == 0:
            return
        # print inFilelist
        for ind in range(len(inFilelist)):
            inFile = inFilelist[ind]
            fmt = readType(cfglist[ind], inFilelist[ind])
            # print fmt
            # xAxis=xAxislist[ind]
            index = colslist[ind]
            cols = []
            # cols.append(xAxis)
            cols.extend(index)
            datalist = np.loadtxt(inFile, unpack=True, usecols=cols)
            # datalist=np.loadtxt(inFile,unpack=True, usecols=cols,dtype=[fmt[col][1] for col in cols])
            str1 = '%d\n'
            if len(cols) > 1:
                x = np.array([i for i in range(1, len(datalist[0]) + 1)])
            else:
                x = np.array([i for i in range(1, len(datalist) + 1)])
            # print type(dlist[0])
            # dlist.insert(0,x)
            dlist = []
            for i in range(len(cols)):
                # print fmt[index[i]]
                if len(cols) > 1:
                    dlist.append(datalist[i])
                else:
                    dlist.append(datalist)
                pic_scale = fmt[index[i]][3]
                if pic_scale != 1.0:
                    line, = self.ax.plot(x, dlist[i] * pic_scale, picker=5, label=fmt[index[i]][0],
                                         linewidth=1)  # ,LineStyle=':',MarkerSymbol='o')
                    self.datalist.extend([x, dlist[i] * pic_scale])
                else:
                    line, = self.ax.plot(x, dlist[i], picker=5, label=fmt[index[i]][0], linewidth=1)
                    self.datalist.extend([x, dlist[i]])
                # line.set_antialiased(False)
                self.linelist.append(line)
                self.lnamelist.append(fmt[index[i]][0])
                # self.datalist.extend([x,dlist[i]])
                if fmt[index[i]][1] not in (np.dtype('float32'), np.dtype('float64')):
                    if fmt[index[i]][2] == 1:
                        str2 = str1 + '0x%x'
                    else:
                        str2 = str1 + '%d'
                else:
                    str2 = str1 + self.annoteLen
                self.fmtlist.append(str2)
        # handles, labels = self.ax.get_legend_handles_labels()
        # print self.fmtlist
        self.browser = PointBrowser(self.fig, self.ax, self.datalist, self.linelist, self.fmtlist)
        plt.grid(True)
        plt.legend(loc=2, prop=zh_font)

    def pic2D(self, inFilelist, cfglist, xAxislist, colslist):
        self.fig, self.ax = plt.subplots(1, 1)
        # print type(self.fig),type(self.ax)
        self.datalist = []
        self.linelist = []
        self.lnamelist = []
        self.fmtlist = []
        zh_font = font_manager.FontProperties(fname=r'c:\windows\fonts\simsun.ttc', size=10)
        if len(inFilelist) == 0:
            return
        # print inFilelist
        for ind in range(len(inFilelist)):
            inFile = inFilelist[ind]
            fmt = readType(cfglist[ind], inFilelist[ind])
            # print fmt
            xAxis = xAxislist[ind]
            index = colslist[ind]
            cols = []
            cols.append(xAxis)
            cols.extend(index)
            dlist = np.loadtxt(inFile, unpack=True, usecols=cols)

            # dlist2=np.loadtxt(inFile,unpack=True)#, usecols=(0,index[0],index[1]))

            # self.ax.set_title('click on point to plot time series')
            # line,line2 = ax.plot(xs, ys,  xs, zs,  picker=5)      #  picker参数必须设置，鼠标的pick_event事件才能激活，数值大小为选取的范围大小
            x = dlist[0]
            if fmt[xAxis][1] not in (np.dtype('float32'), np.dtype('float64')):
                str1 = '%d\n'
            else:
                # str1='%.4e\n'
                str1 = self.annoteLen + '\n'

            for i in range(len(cols) - 1):
                pic_scale = fmt[index[i]][3]  # 20170507  i修改为index[i]，修复bug
                # print pic_scale
                if pic_scale != 1.0:
                    line, = self.ax.plot(x, dlist[i + 1] * pic_scale, picker=5, label=fmt[index[i]][0],
                                         linewidth=1)  # ,LineStyle=':',MarkerSymbol='o')
                    self.datalist.extend([x, dlist[i + 1] * pic_scale])  # 20170507  此处必须将刻度值乘到数据中，否则点标注将显示原有点的值
                else:
                    line, = self.ax.plot(x, dlist[i + 1], picker=5, label=fmt[index[i]][0], linewidth=1)
                    self.datalist.extend([x, dlist[i + 1]])
                # line.set_antialiased(False)
                self.linelist.append(line)
                self.lnamelist.append(fmt[index[i]][0])
                # self.datalist.extend([x,dlist[i+1]])  #  20170507  注释
                if fmt[index[i]][1] not in (np.dtype('float32'), np.dtype('float64')):
                    if fmt[index[i]][2] == 1:
                        str2 = str1 + '0x%x'
                    else:
                        str2 = str1 + '%d'
                else:
                    # str2=str1+'%.4e'
                    str2 = str1 + self.annoteLen
                self.fmtlist.append(str2)
        # handles, labels = self.ax.get_legend_handles_labels()
        # print self.fmtlist
        self.browser = PointBrowser(self.fig, self.ax, self.datalist, self.linelist, self.fmtlist)
        plt.grid(True)
        plt.legend(loc=2, prop=zh_font)


    def anoteset(self):
        if self.anoteAction.isChecked():
            self.pickCid = self.fig.canvas.mpl_connect('pick_event', self.browser.onpick)
            self.keyCid = self.fig.canvas.mpl_connect('key_press_event', self.browser.onpress)
            self.browser.setDraggable(True)
            # QAction().isChecked()
        else:
            self.browser.setDraggable(False)
            self.fig.canvas.mpl_disconnect(self.pickCid)
            self.fig.canvas.mpl_disconnect(self.keyCid)

    def chklistSlot(self):
        self.browser.hideline = []
        for index in range(len(self.chklist)):
            # x=QCheckBox()
            if self.chklist[index].checkState() == 0:
                # print self.linelist[index].get_visible()
                # self.anotBackup[index]=[]
                self.linelist[index].set_visible(False)
                self.browser.hideline.append(index)  # 隐藏的线段添加到browser对象中的hideline，不再对其进行标注
                for point in self.browser.datapick[index]:
                    # text=self.browser.datapick[index][point][0]._text
                    # self.anotBackup[index].append(text)
                    self.browser.datapick[index][point][0].set_visible(False)
                    self.browser.datapick[index][point][1].set_visible(False)
            else:
                self.linelist[index].set_visible(True)
                if index in self.browser.hideline:  # 被隐藏的线段恢复可标注
                    self.browser.hideline.remove(index)
                for point in self.browser.datapick[index]:
                    # text=self.browser.datapick[index][point][0]._text
                    # self.anotBackup[index].append(text)
                    self.browser.datapick[index][point][0].set_visible(True)
                    self.browser.datapick[index][point][1].set_visible(True)
        # print self.browser.hideline
        self.on_draw()

        # def __del__(self):

    # # self.fig,self.ax,self.datalist,self.linelist,self.fmtlist
    # self.browser.dataset=None
    # self.browser.lineset=None
    #     self.browser.fmt=None
    #     self.datalist=None
    #     self.linelist=None
    #     self.fmtlist=None
    #     gc.collect()
    def exitslot(self):
        # self.browser.dataset=None
        # self.browser.lineset=None
        # self.browser.fmt=None
        # self.datalist=None
        # self.linelist=None
        # self.fmtlist=None
        del self.browser.dataset
        del self.browser.lineset
        del self.browser.fmt
        del self.datalist
        del self.linelist
        del self.fmtlist

        self.fig.clf(True)
        del self.fig

        del self.ax
        del self.canvas

        gc.collect()
        # self.emit(SIGNAL('_signalexit'))
        # self.close()

    def testslot(self):
        print('slot trigger!')


def readType(cfg_name, file):
    # sty_dict={0:'int32',1:'int32',2:'float',3:'float',4:'float',5:'int32',6:'int32',7:'int32',8:'int32'}
    # sty_dict={0:'i',1:'u',2:'f',3:'f',4:'d',5:'i',6:'u',7:'i',8:'u'}
    sty_dict = {0: np.int32, 1: np.uint32, 2: np.float32, 3: np.float32, 4: np.float64, 5: np.int16, 6: np.uint16,
                7: np.int8, 8: np.int8}
    type = []
    if cfg_name == '':
        line = open(file).readline()
        line = line.split()
        for i in range(len(line)):
            type.append((str(i), np.float32, 0, 1.0))

    else:
        db = shelve.open('config')
        cfg = db['frame_dict'][cfg_name]
        # type=[]
        item_dict = cfg.frame_datCfg_dict
        for item in cfg.frame_datCfg_list:
            type.append((
                item, sty_dict[item_dict[item].dataStyle], item_dict[item].disp, item_dict[item].scale))  # 新增scale，画图比例
        # print type
        db.close()
    # print type[:10]
    return type


def main():
    app = QApplication(sys.argv)
    # form = AppForm('test.dat',u'21ca-mid',0,[90,91,92])
    # form = AppForm(['test.dat'],[u'21ca-mid'],[0],[[170,171,172]])
    form = AppForm(['test.dat'], [u'camid'], [[1, 2, 3]], [0], D1_flag=False)
    # form = AppForm(['test.dat'],[u'camid'],[[1,2,3]],D1_flag=True)
    form.show()
    app.exec_()


if __name__ == "__main__":
    main()
