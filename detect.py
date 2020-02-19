# -*- coding: utf-8 -*-
import sys, os, re

# 检测字符串是否为16进制数
def ishex(str):
    if str.startswith('0x'):
        str = str[2:]
    elif str.startswith('0X'):
        str = str[2:]
    if re.findall(r'[^0-9a-fA-F]', str) != []:
        return False
    else:
        return True