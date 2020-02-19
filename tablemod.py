# -*- coding: utf-8 -*-
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
import numpy as np


class MyTableModel(QAbstractTableModel):
    def __init__(self, datain, headlist, linecnt, hexcols, parent=None, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.arraydata = datain
        self.columns = len(self.arraydata[0])
        self.hexcl = hexcols  # 需要以16进制显示的列(列号的list)
        # print headlist
        if headlist == [] or headlist == 0:
            self.headers = {i: str(i + 1) for i in range(self.columns)}
        elif len(headlist) != self.columns:
            self.headers = {i: headlist[i] for i in range(self.columns)}
        else:
            self.headers = {i: headlist[i] for i in range(self.columns)}
        # self.headlist = ['head'+str(i) for i in range(80)]
        self.index = -1
        self.linecnt = linecnt
        self.pagecnt = int(linecnt / 4000)
        if self.pagecnt * 4000 < linecnt:
            self.pagecnt += 1
        print('>> %d 行，%d 页  ' % (linecnt, self.pagecnt))
        self.pageindex = 0

    def updateModel(self, delCount):  # 用户删除数据文件中某些行后，重新更新Model中的重要值 delCount=删除的总行数
        self.linecnt -= delCount
        self.pagecnt = int(self.linecnt / 4000)
        if self.pagecnt * 4000 < self.linecnt:
            self.pagecnt += 1
        if self.pageindex >= self.pagecnt:
            self.pageindex = self.pagecnt - 1

    def rowCount(self, parent):
        # return len(self.arraydata[0])
        # self.rows
        return len(self.arraydata)
        # return 10000

    def columnCount(self, parent):
        # return len(self.arraydata)
        return len(self.arraydata[0])

    def headerData(self, column, orientation, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return QVariant()
        if orientation == Qt.Horizontal:
            if column >= self.columns:
                return QVariant()
            return self.headers[column]
        return QVariant()

    def setHeaderData(self, column, orientation, value, role=Qt.EditRole):
        self.headers[column] = value
        pass

    def data(self, index, role):
        if not index.isValid():
            return QVariant()
        elif role != Qt.DisplayRole:
            return QVariant()
        tmp = self.arraydata[index.row()][index.column()]
        if index.column() in self.hexcl:
            tmp = '%#-12x' % (eval(tmp))
        return QVariant(tmp)
        # return QVariant(self.arraydata[index.column()][index.row()])

    def removeRows(self, row, count, parent=QModelIndex()):
        self.beginRemoveRows(parent, row, row + count - 1)
        for i in reversed(range(count)):
            self.arraydata.pop(row + i)
        self.endRemoveRows()
        return True

    def moveRows(self):
        pass

