# coding:utf-8
import struct, shelve, shutil
from random import randint

fmt = '>Iifhb'

head = 0xaabbccdd


def DataGenerate(fil, fmt, head):
    with open(fil, 'wb') as f:
        for i in range(10000):
            tmp = [head, randint(-1000000, 1000000), randint(100, 1000) / 10.0, randint(-32768, 32767),
                   randint(-127, 127)]
            x = struct.pack(fmt, *tmp)
            f.write(x)
            pass


if __name__ == "__main__":
    f = 'data2.dat'
    # DataGenerate(f,fmt,head)
    # f=shelve.open('config')
    # for i in f.keys():
    # print(i)
    # a=f['frame_dict']['aaa'].frame_head
    shutil.copyfile('814.txt', '814n.txt')
    with open('814.txt', 'r') as fp:
        a = fp.readlines()
    with open('814.txt', 'w') as fp:
        for l in a:
            fp.write(l)