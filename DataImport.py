# -*- coding: utf-8 -*-

import sys, os, string, shutil
import csv, shelve
import struct
# import datetime

sty_dict = {0: 'I', 1: 'i', 2: 'f', 3: 'fx',
            4: 'd', 5: 'H', 6: 'h', 7: 'B', 8: 'b'}

disp_dict = {(0, 0): '%-12d', (0, 1): '%-12d', (0, 2): '%-15.6e', (0, 3): '%-17.8e', (0, 4): '%-17.8e', (0, 5): '%-12d',
             (0, 6): '%-12d', (0, 7): '%-12d', (0, 8): '%-12d',
             (1, 0): '%#-12x', (1, 1): '%#-12x', (1, 2): '%-15.6e', (1, 3): '%-17.8e', (1, 4): '%-17.8e',
             (1, 5): '%#-12x', (1, 6): '%#-12x', (1, 7): '%#-12x', (1, 8): '%#-12x'}

len_dict = {0: 4, 1: 4, 2: 4, 3: 5,
            4: 8, 5: 2, 6: 2, 7: 1, 8: 1}

# def print_check(x,str):
# if x==None:
# print str
# else:
#         print str,x

# 二进制文件的读取和分析
def ReadBfile(path, cfg, dfile):
    f = open(path, 'rb')
    (head, fmt, dispfmt, DataLen) = cfg
    res = open(dfile, 'w')  # 解析结果存在dfile中
    # head=struct.pack('>I',eval(head))   # 目前均按大端序处理
    # print(head.hex())
    f.seek(0, 2)  # 获取文件长度，字节数
    end = f.tell()
    f.seek(0, 0)

    Hlen = len(head)  # 帧头占用字节数
    readlenth = DataLen
    offset1 = 1 - Hlen
    offset2 = Hlen - readlenth
    content = f.read(readlenth)
    head = bytes().fromhex(head.hex())
    fstart = content.find(head)
    # print end
    tmp = dispfmt.split('%')[1:]  #  dispfmt以%起始，导致tmp第一个元素为''
    hexcols = []
    for index in range(len(tmp)):
        if tmp[index].startswith('#'):
            hexcols.append(index)

    # dispfmt1=string.replace(dispfmt,'#-12x','-12d')
    dispfmt1 = dispfmt.replace('#-12x', '-12d')
    fptr = f.tell()
    while fptr < end:
        if fstart != -1:
            f.seek(fstart + offset2, 1)
            frm = f.read(readlenth)
            # str=dispfmt % struct.unpack(fmt,frm)
            str2 = dispfmt1 % struct.unpack(fmt, frm)
            res.write(str2)
            content = f.read(readlenth)
            fstart = content.find(head)
            fptr = f.tell()
        else:
            f.seek(offset1, 1)
            # content=f.read(100)
            content = f.read(readlenth)
            fstart = content.find(head)
            fptr = f.tell()
    f.close()
    res.close()
    # print hexcols
    return hexcols


# 解析配置项的内容
def CfgProcess(cfg_name):
    db = shelve.open('config')
    cfg = db['frame_dict'][cfg_name]
    # cfg=cfg_name
    # print type(cfg),cfg
    if cfg.frame_endian == 0:  # 20200209 修改为处理大小端
        sty = '>'
    else:
        sty = '<'
    disp_fmt = ''
    Dlen = 0
    headtmp = cfg.frame_head[2:]
    # frame_head  帧头处理位二进制 ：0xFFBBBBFF -> '\xff\xbb\xbb\xff'    20170902
    # head = ''.join([struct.pack('B',eval('0x'+headtmp[i:i+2])) for i in range(0,len(headtmp),2)])
    head = bytes().fromhex(headtmp)
    # tail = cfg.frame_tail                   # frame_tail  帧尾  utf8 编码的16进制数字字符串，含0x
    # trans = cfg.frame_trans                 # frame_trans  转义  utf8 编码的16进制数字字符串列表，含0x
    item_dict = cfg.frame_datCfg_dict
    displist = []
    for item in cfg.frame_datCfg_list:  # frame_datCfg_list 数据域的名称列表  unicode编码
        sty = sty + sty_dict[item_dict[item].dataStyle]
        disp_fmt = disp_fmt + disp_dict[(item_dict[item].disp, item_dict[item].dataStyle)]
        Dlen = Dlen + len_dict[item_dict[item].dataStyle]
        displist.append(item_dict[item].disp)
    db.close()
    return (head, sty, disp_fmt + '\n', Dlen)


# 将纯文本中含有16进制的列替换为10进制表示  20170814
def DataFileReplace(file, cols=None):
    resfile = 'tempFile\\' + os.path.splitext(os.path.basename(file))[0] + 'temp.txt'
    if cols:
        # print resfile
        res = open(resfile, 'w')
        with open(file) as f:
            for line in f:
                line = line.split()
                for ind in cols:
                    line[ind] = str(eval(line[ind]))
                newline = '    '.join(line) + '\n'
                res.write(newline)
        res.close()
    else:
        shutil.copyfile(file, resfile)
    return resfile


# 16进制表示的文本文件的读取和分析
def ReadHexfile(path, cfg, dfile):
    pass


def Hex2Bin(file, res):
    f = open(file, 'r')
    r = open(res, 'wb')
    contents = f.readlines()
    j = 0
    linetmp = ''
    for line in contents:
        j += 1
        tmp = line.split()
        try:
            linetmp += ''.join([struct.pack('B', eval('0x' + i)) for i in tmp])
        except:
            print(">> 文件含有非法数据，请检查！")
            break
    r.write(linetmp)
    # print j,len(line.split())
    f.close()
    r.close()
    pass


def headCheck(fp, head, start=0):
    pass


# CSV文件的1553数据分离为二进制文件
def D1553Separation(datafile, MsgID, hlist):
    namelist = [item[1:-1] + '.dat' for item in MsgID]
    with open(datafile) as f:
        # f_csv=csv.reader(f)
        # headers=next(f_csv)
        # f_csv=csv.DictReader(f)
        resFlist = []
        dCntlist = []
        headlist = headtransform(hlist)
        fmtlist = []
        endlist = []
        try:
            for id in MsgID:
                name = id[1:-1]
                ftmp = open('1553B' + os.sep + name + '.dat', 'wb')
                resFlist.append(ftmp)
                datacnt = eval(name.split('-')[-1])
                if datacnt == 0: datacnt = 32
                dCntlist.append(datacnt)
                fmtlist.append('>' + 'H' * datacnt)
                endlist.append(10 + datacnt)
        except:
            print('>> 输入ID错误，请检查！')
            return
        f.readline()
        for row in f:
            rtmp = row.split(',')
            if rtmp[6] in MsgID:
                idx = MsgID.index(rtmp[6])
            elif rtmp[8] in MsgID:
                idx = MsgID.index(rtmp[8])
            else:
                continue
            tmp = headlist[idx]
            tmpdata = [eval(j) for j in rtmp[10:endlist[idx]]]
            tmp += struct.pack(fmtlist[idx], *tmpdata)
            resFlist[idx].write(tmp)
            # if row['Rx Summary'] in MsgID:
            #     idx=MsgID.index(row['Rx Summary'])
            #     tmp=headlist[idx]
            #     for i in range(dCntlist[idx]):
            #         Dindex = 'D'+str(i+1)
            #         tmp += struct.pack('>H',eval(row[Dindex]))
            #     resFlist[idx].write(tmp)
        for resf in resFlist:
            resf.close()
        print('>> 解析完成，结果存储于本软件路径"1553B\"文件夹下!')
        x = '|File: |' + ' %-18s|' * len(namelist) % tuple(namelist)
        print('-' * len(x))
        print(x)
        print('-' * len(x))
        x = '|Head: |' + ' %-18s|' * len(hlist) % tuple(hlist)
        print(x)
        print('-' * len(x))


# 获取帧头二进制： ['0xffaaaaff'] -> ['\xff\xaa\xaa\xff']
def headtransform(headlist):
    res = []
    for headstr in headlist:
        head = headstr[2:]
        headsplit = [head[i:i + 2] for i in range(0, len(head), 2)]
        tmp = ''.join([struct.pack('B', eval('0x' + i)) for i in headsplit])
        res.append(tmp)
    return res


def headget(length):
    head = []
    for i in range(length):
        stmp = '0xff%sff' % ((hex(i + 1)[2:]) * 4)
        head.append(stmp)
    return head
    pass


if __name__ == '__main__':
    pass
    # x=u'KT-3'
    # ReadBfile('KT-3.bin',x,'test.dat')
    # CfgProcess(x)
    # import random
    # DataFileReplace('subfile.txt',[170,171,172])
    # f=open('hexfile903.txt','w')
    # for i in range(100):
    #     for j in range(100):
    #         x = random.randint(0,255)
    #         f.write(hex(x)[2:]+'\t')
    #     f.write('\n')

    # Hex2Bin('hexfile903.txt','hexfileBIN.dat')
    # f= open('hexfileBIN.dat')
    # x=f.read(10000)
    #
    # # f.seek(0,2)
    # print f.tell()
    # tmp=[i for i in x]
    # print tmp
    # print len(x),len(tmp)
