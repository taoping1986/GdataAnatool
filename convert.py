# coding:utf-8
import struct


def floattoHex(val, ending=0):
    if ending == 1:
        # x=struct.pack('<f',val).encode('hex')
        x = struct.pack('<f', val)
        # x.decode('utf-8')
    else:
        # x=struct.pack('>f',val).encode('hex')
        x = struct.pack('>f', val)
        # x.decode('utf-8')
    return x.hex()


def hextoFloat(valstr, ending=0):
    # valstr = string.replace(valstr,'0x','')
    valstr = valstr.replace('0x', '')
    if ending == 1:
        # return struct.unpack('<f',valstr.decode('hex'))[0]
        return struct.unpack('<f', bytes.fromhex(valstr))[0]
    else:
        # return struct.unpack('>f',valstr.decode('hex'))[0]
        return struct.unpack('>f', bytes.fromhex(valstr))[0]
