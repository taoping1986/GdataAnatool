# -*- coding: utf-8 -*-
import numpy as np
# import matplotlib.widgets as wid
import shelve

# import matplotlib
# matplotlib.use("Qt4Agg")
# from matplotlib.figure import Figure
# from matplotlib.backend_bases import key_press_handler
# from matplotlib.backends.backend_qt4agg import (
# FigureCanvasQTAgg as FigureCanvas,
# NavigationToolbar2QT as NavigationToolbar)
import matplotlib.pyplot as plt
# import matplotlib.patches as mpatch
# import random
from matplotlib import font_manager
# from matplotlib.backends import qt_compat
# use_pyside = qt_compat.QT_API == qt_compat.QT_API_PYSIDE
import gc
# from PyQt4.QtCore import *
# from PyQt4.QtGui import *
# from embedding_in_qt4_wtoolbar import *
class PointBrowser(object):
    """
    Click on a point to select and highlight it -- the data that
    generated the point will be shown in the lower axes.  Use the 'd'
    and 'a' keys to browse through the next and previous points
    """
    # def __init__(self,fig,ax,x,y,z,dataset=None,lineset=None):
    def __init__(self, fig, ax, dataset=None, lineset=None, fmt=None):
        self.lastind = 0
        self.ax = ax
        self.fig = fig
        self.dataset = dataset  # 数据集合
        self.lineset = lineset  # 曲线集合
        self.fmt = fmt
        self.datapick = {i: {} for i in
                         range(len(self.lineset))}  # 用于存储每条曲线已选的点 {line(i){index:(annote,pickpoint)....}}
        self.lastind = None
        self.offset = 0
        self.picknow = -1
        self.hideline = []  # 隐藏的线的index集合，该列表的线段不进行标注，在调用该类的对象中进行添加和删除

    def onpress(self, event):  # (d,a)按键检测及响应
        if self.lastind is None:
            return
        if event.key not in ('d', 'a', 't'):
            return
        if self.picknow in self.hideline:
            return
        if event.key == 'd':  #  d键 显示下一点坐标
            inc = 1
        elif event.key == 'a':  #  a键 显示上一点坐标
            inc = -1
        elif event.key == 't':
            self.setDraggable(False)
            return
        prevIndex = self.lastind
        self.lastind += inc
        self.lastind = np.clip(self.lastind, 0, len(self.dataset[self.offset]) - 1)
        # print 'keyPress:'
        # print self.datapick[self.pickindex]
        if prevIndex in self.datapick[self.picknow].keys():  # 清除上一点的标注
            # print self.datapick[self.picknow].keys()
            x = self.datapick[self.picknow].pop(prevIndex)
            x[0].set_text('')
            x[1].set_visible(False)
            del x[0]
            del x[0]
            gc.collect()
        if self.lastind in self.datapick[self.picknow].keys():  #  若新的点已标注，则直接更新画图并退出
            self.fig.canvas.draw()
            return
        self.pickindex = self.picknow  # 容错性，规避了一个bug，不能删除  20170216
        self.update()

    def onpick(self, event):  # 鼠标点击事件
        self.pickindex = -1
        # print
        # print self.lineset
        if event.artist in self.lineset:
            # print "choose",event.artist
            self.pickindex = self.lineset.index(event.artist)  # 确定选择了图中哪条曲线
            self.picknow = self.pickindex  # 容错性设计，用于类中某些成员的下标，保证当前选择有确定的对象，避免出现keyerr
            if self.pickindex in self.hideline:  # 如果选择了隐藏的线段，则直接返回
                return True
        else:
            self.pickindex = -1
            return True
        # print self.pickindex
        N = len(event.ind)  # event.ind为选取的点在数据中的索引，可能不止一个
        if not N:
            return True
        # the click locations  鼠标点击点的坐标
        x = event.mouseevent.xdata
        y = event.mouseevent.ydata

        self.offset = 2 * self.pickindex
        self.posx = x
        self.posy = y
        # print x,y
        distances = np.hypot(x - self.dataset[self.offset][event.ind],
                             y - self.dataset[self.offset + 1][event.ind])  # 计算鼠标选取的点离鼠标点击位置的距离
        indmin = distances.argmin()  # 计算鼠标选取的点离鼠标点击位置的距离
        dataind = event.ind[indmin]  # 得到距离最小的点
        self.lastind = dataind  # 得到距离最小的点的索引
        self.update()

    def update(self):  # 点标注及画布更新
        if self.lastind is None:
            return
        dataind = self.lastind
        if dataind in self.datapick[self.pickindex].keys():
            x = self.datapick[self.pickindex].pop(dataind)
            x[0].set_text('')
            x[1].set_visible(False)
            # x[0].arrow_patch.set_arrowstyle('-')
            self.fig.canvas.draw()
            return
        selected, = self.ax.plot([self.dataset[self.offset][dataind]], [self.dataset[self.offset + 1][dataind]], 'o',
                                 ms=5, alpha=0.7,
                                 color='black', visible=False)
        selected.set_visible(True)
        # x = plt.annotate('%.4e\n%.4e' % (self.dataset[self.offset][dataind], self.dataset[self.offset+1][dataind]),
        #           xy=(self.dataset[self.offset][dataind], self.dataset[self.offset+1][dataind]),
        #           xytext=(self.dataset[self.offset][dataind], self.dataset[self.offset+1][dataind]),
        #           size=20, #va="center", ha="center",
        #           bbox=dict(boxstyle="square", fc="w",ec="0.5",alpha=0.7),
        #           verticalalignment="bottom",horizontalalignment="right",)
        if self.fmt[self.picknow].endswith("%x"):
            point = (self.dataset[self.offset][dataind],
                     int(self.dataset[self.offset + 1][dataind]))  # for python3 : change to int
        else:
            point = (self.dataset[self.offset][dataind], self.dataset[self.offset + 1][dataind])
        x = plt.annotate(self.fmt[self.picknow] % point,
                         xy=point,
                         xytext=point,
                         size=20,  #va="center", ha="center",
                         bbox=dict(boxstyle="square", fc="w", ec="0.5", alpha=0.7),
                         verticalalignment="bottom", horizontalalignment="right", )
        # x = plt.annotate(self.fmt[self.picknow] % (self.dataset[self.offset][dataind], self.dataset[self.offset+1][dataind]),
        #           xy=(self.dataset[self.offset][dataind], self.dataset[self.offset+1][dataind]),
        #           xytext=(self.dataset[self.offset][dataind], self.dataset[self.offset+1][dataind]),
        #           size=20, #va="center", ha="center",
        #           bbox=dict(boxstyle="square", fc="w",ec="0.5",alpha=0.7),
        #           verticalalignment="bottom",horizontalalignment="right",)

        x.set_fontsize(8)
        x.draggable(True, True)
        self.datapick[self.pickindex][dataind] = [x, selected]
        self.fig.canvas.draw()

    def setDraggable(self, enable=True):
        if enable == True:
            for line in self.datapick:
                for point in self.datapick[line]:
                    self.datapick[line][point][0].draggable(True, True)
        elif enable == False:
            for line in self.datapick:
                for point in self.datapick[line]:
                    self.datapick[line][point][0].draggable(False, False)
        else:
            return


# ***********************************************
# 单个文件的二维图
# inFile：数据文件
# cfg：   配置名
# xAxis:  x轴的所用数据列号，example: 0
# index:  y轴的数据列号 ,example: [10,11,12]
# ***********************************************
def pic1D(inFile, cfg, xAxis, index):
    fmt = readType(cfg)
    print(fmt)
    cols = []
    cols.append(xAxis)
    cols.extend(index)
    dlist = np.loadtxt(inFile, unpack=True, usecols=cols)
    # dlist2=np.loadtxt(inFile,unpack=True)#, usecols=(0,index[0],index[1]))
    fig, ax = plt.subplots(1, 1)
    # ax.set_title('click on point to plot time series')
    # line,line2 = ax.plot(xs, ys,  xs, zs,  picker=5)      #  picker参数必须设置，鼠标的pick_event事件才能激活，数值大小为选取的范围大小
    x = dlist[0]
    datalist = []
    linelist = []
    zh_font = font_manager.FontProperties(fname=r'c:\windows\fonts\simsun.ttc', size=10)
    for i in range(len(cols) - 1):
        line, = ax.plot(x, dlist[i + 1], picker=5, label=fmt[index[i]][0])
        linelist.append(line)
        datalist.extend([x, dlist[i + 1]])
    handles, labels = ax.get_legend_handles_labels()
    browser = PointBrowser(fig, ax, datalist, linelist)

    # fig.canvas.mpl_connect('pick_event', browser.onpick)
    # fig.canvas.mpl_connect('key_press_event', browser.onpress)

    plt.grid(True)
    plt.legend(loc=2)
    # app = QApplication(sys.argv)
    # form = AppForm(fig,ax,linelist,datalist)
    # form.show()
    # app.exec_()
    plt.show()
    # return browser


def readType(cfg_name):
    # sty_dict={0:'int32',1:'int32',2:'float',3:'float',4:'float',5:'int32',6:'int32',7:'int32',8:'int32'}
    # sty_dict={0:'i',1:'u',2:'f',3:'f',4:'d',5:'i',6:'u',7:'i',8:'u'}
    sty_dict = {0: np.int32, 1: np.uint32, 2: np.float32, 3: np.float32, 4: np.float64, 5: np.int16, 6: np.uint16,
                7: np.int8, 8: np.int8}
    db = shelve.open('config')
    cfg = db['frame_dict'][cfg_name]
    type = []
    item_dict = cfg.frame_datCfg_dict
    for item in cfg.frame_datCfg_list:
        type.append((item, sty_dict[item_dict[item].dataStyle]))
    # print type
    return type


if __name__ == '__main__':
    # pic1D('test.dat',u'21ca-mid',0,[13,14,15])
    # pic1D('test.dat',u'21ca-mid',0,[31,32,33])
    pic1D('test.dat', u'21ca-mid', 0, [31, 32, 33])
    # x=input()
    # brw.setDraggable(False)
    # pic1D('test.dat','',0,[17,18])
    # x=input()
    # pic1D('test.dat','',0,[12,14])
    # x=input()
    # pic1D('test.dat','',0,[15,16])
    # x=input()
    # pic1D('test.dat','',0,[10,11])
    # x=input()
    # pic1D('test.dat','',0,[170,171])

