# coding:utf-8
import os
import numpy as np
import subprocess
# f=open('Kstate1.txt')
S2_on_mock = 0
S2_off_mock = 0
S3_off_mock = 0
S3_on_mock = 0
state_on_mock = 0
state_off_mock = 0
bit_flag = False
cnt = 0
result = []


def state_analyze(x_axis, column, file, config):
    global state_on_mock, state_off_mock, bit_flag
    state_on_mock = 0
    state_off_mock = 0
    # print column
    # print "start analyze %s!!!" % (file)
    # f='bitana.txt'

    resfile = open('bitana.txt', 'w')
    printflag = False
    if x_axis is not None:
        f = open(file)
        line = f.readline()
        line = line.split()
        # if type(eval(line[x_axis]))==type(0.0):
        if '.' in line[x_axis]:  # x轴是否为浮点数
            loadfmt = ('f4', 'u4')
            printfmt = "%-8.4e    %s\n"
        else:
            loadfmt = ('i4', 'u4')
            printfmt = "%-8d    %s\n"
        f.close()
        printflag = True
        [x_ax, Data] = np.loadtxt(file, dtype={'names': ('X', 'Data'),
                                               'formats': loadfmt},
                                  unpack=True,
                                  usecols=[x_axis, column])  # 20170814  i4->I4  signed 修改为unsigned   防止读取数据时溢出
        bit_flag = True
    else:
        Data = np.loadtxt(file, dtype='u4', unpack=True, usecols=[column])
        x_ax = range(len(Data))
        bit_flag = False
        printfmt = "Line: %6d     %s\n"
    count = len(Data)
    # print config
    prevdata = None
    for i in range(count):
        t = x_ax[i]
        s = Data[i]
        tmp = []
        flag = False
        for x in config.keys():
            item = config[x]
            if 1 in item.keys():
                if item[1] != '':
                    res = state1_judge(t, s, x, item[1], prevdata)
                    if res is not None:
                        tmp.append(res)
                        flag = True
            if 0 in item.keys():
                if item[0] != '':
                    res = state0_judge(t, s, x, item[0], prevdata)
                    if res is not None:
                        tmp.append(res)
                        flag = True
        if flag:
            strtmp = len(tmp) * "%10s, " % tuple(tmp)
            if printflag:
                resline = printfmt % (t, strtmp)
            else:
                resline = printfmt % (t + 1, strtmp)
            resfile.write(resline)
            prevdata = s
        else:
            prevdata = s
    resfile.close()
    # os.system('bitana.txt')
    subprocess.Popen(["notepad.exe", "bitana.txt"])
    print('>> Bit Analyze Done!')


def state1_judge(t, sta, bit, sx, prev):
    if prev is not None:
        if bittest(sta, bit) == bittest(prev, bit):
            return
        elif bittest(sta, bit) == 1:
            return sx
        else:
            return
    elif bittest(sta, bit) == 1:
        return sx
    else:
        return


def state0_judge(t, sta, bit, sx, prev):
    if prev is not None:
        if bittest(sta, bit) == bittest(prev, bit):
            return
        elif bittest(sta, bit) == 0:
            return sx
        else:
            pass
    elif bittest(sta, bit) == 0:
        return sx
    else:
        return


def bittest(data, pos):
    if data & (1 << pos) == 0:
        return 0
    else:
        return 1


# def state1_judge(t,sta,bit,sx):
# global state_on_mock,state_off_mock,result
# if (state_on_mock & (1<<bit))==0:
#         if (sta & (1<<bit))!=0:
#             # x='%-8.2f %-15s' % (t/100.0,'   '+sx)
#             if bit_flag:
#                 x='     %-8.2f %-15s' % (t,'   '+sx)
#             else:
#                 x='     Line: %-8d %-15s' % (t+1,'   '+sx)
#             print x
#             # result.append(x)
#             state_on_mock=state_on_mock | (1<<bit)
#
# def state0_judge(t,sta,bit,sx):
#     global state_on_mock,state_off_mock
#     if (state_on_mock & (1<<bit))!=0 and (state_off_mock & (1<<bit))==0:
#         if (sta & (1<<bit))==0:
#             if bit_flag:
#                 x='     %-8.2f %-15s' % (t,'   '+sx)
#             else:
#                 x='     Line: %-8d %-15s' % (t+1,'   '+sx)
#             print x
#             # result.append(x)
#             state_off_mock=state_off_mock | (1<<bit)

# 值域分析函数
def value_analyze(x_axis, column, file, config):
    if x_axis is not None:
        f = open(file)
        line = f.readline()
        line = line.split()
        # if type(eval(line[x_axis]))==type(0.0):
        if '.' in line[x_axis]:  # x轴是否为浮点数
            loadfmt = ('f4', 'u4')
            printfmt = '%-20f0x%-20X%s\n'

        else:
            loadfmt = ('i4', 'u4')
            printfmt = '%-20d0x%-20X%s\n'

        f.close()

        [x_ax, Data] = np.loadtxt(file, dtype={'names': ('X', 'Data'),
                                               'formats': loadfmt},
                                  unpack=True, usecols=[x_axis, column])
        # fmt='     %-20f%-20d%s'

    else:
        Data = np.loadtxt(file, dtype='u4', unpack=True, usecols=[column])
        x_ax = range(len(Data))
        # fmt='     Line: %-20d%-20d%s'
        printfmt = 'Line: %-20d0x%-20X%s\n'
    resf = open("valueAna.txt", "w")
    count = len(Data)
    currentVal = None
    for i in range(count):
        t = x_ax[i]
        s = Data[i]
        if s in config.keys() and s != currentVal:
            tmpstr = printfmt % (t, s, config[s])
            resf.write(tmpstr)
            currentVal = s
            # print 'cur'+str(currentVal)
    resf.close()
    subprocess.Popen(["notepad.exe", 'valueAna.txt'])
    print('>> Value Analyze Done!')

# def value_analyze(x_axis,column,file,config):
#     if x_axis is not None:
#         [x_ax,Data]=np.loadtxt(file,dtype={'names': ('X', 'Data'),
#                                      'formats': ('f4', 'u4')},
#                          unpack=True, usecols=[x_axis,column])
#         # fmt='     %-20f%-20d%s'
#         fmt='     %-20f0x%-20X%s'
#     else:
#         Data = np.loadtxt(file,dtype='I4',unpack=True, usecols=[column])
#         x_ax = range(len(Data))
#         # fmt='     Line: %-20d%-20d%s'
#         fmt='     Line: %-20d0x%-20X%s'
#
#     count = len(Data)
#     currentVal=None
#     for i in range(count):
#         t=x_ax[i]
#         s=Data[i]
#         if s in config.keys() and s!=currentVal:
#             print fmt % (t,s,config[s])
#             currentVal=s
#             # print 'cur'+str(currentVal)
#     print '>> Value Analyze Done!'
# monkeys=[i+1 for i in range(10)]
# out_n=5
# def monkeyking(start,out_n,monkeys):
#     leftcount=len(monkeys)
#     if leftcount==1:
#         print monkeys[0]
#         return monkeys[0]
#     else:
#         outindex=(start+out_n%leftcount-1)%leftcount
#         monkeys.pop(outindex-1)
#         # print outindex
#         if outindex==0:
#             outindex=1
#         # print outindex,monkeys
#         monkeyking(outindex,out_n,monkeys)
#
# def king(m,n):
#     dd = {}
#     #生成一个字典
#     p = 1
#     while(p<=m):
#         dd[p] = p
#         p = p+1
#
#     j = 1
#     while(len(dd) >1):
#         for k,v in dd.items():
#             if(j == n):
#                 del dd[k]
#                 j = 1
#             else:
#                 j = j+1
#     return dd

if __name__ == '__main__':
    file = 'test.dat'
    file = 'subfile.txt'
    # Data = np.loadtxt(file,dtype='I4',unpack=True, usecols=[105])
    # print Data[:10]
    x = ['t0', 'zk1_on', 'tjd1_off']
    ss = tuple(x)
    fmt = len(x) * "%-15s"
    # s="%-15s%-15s%-15s" % ss
    s = len(x) * "%-15s" % tuple(x)
    print(s)

    # file = 'fsfy2.txt'
    # f=open(file,'w')
    # for i in range(2000):
    #     x=str(i)
    #     l='    %s    %s     %s\n' % (x,x,x)
    #     f.write(l)
    # f.close()
    # monkeys=[i+1 for i in range(10)]
    # out_n=106
    # monkeyking(1,out_n,monkeys)
    #
    #
    # y=king(10,106)
    # print y