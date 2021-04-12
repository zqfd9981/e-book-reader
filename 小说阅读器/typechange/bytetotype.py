"""
类型转化函数，将收到封装的byte转化为'int'等类型
"""
import socket

import enum
from struct import pack, unpack
from typechange.message_type import MessageType
from binascii import unhexlify


def long_to_bytes(val, endianness='big'):
    """
    将数字转化为byte
    """

    width = val.bit_length()
    width += 8 - ((width % 8) or 8)

    fmt = '%%0%dx' % (width // 4)

    s = b'\x00' if fmt % val == '0' else unhexlify(fmt % val)

    if endianness == 'little':
        s = s[::-1]

    return s


def _deserialize_any(bytes):
    byte_reader = ByteArrayReader(bytes)
    type = byte_reader.read(1)[0]
    if type == 0:
        return None

    body_len = int.from_bytes(byte_reader.read(4), 'big')
    return typeset[type](byte_reader.read(body_len))


def deserialize_message(data):
    ret = {}
    byte_reader = ByteArrayReader(data)
    ret['type'] = get_message_type_from_value(byte_reader.read(1)[0])
    ret['parameters'] = _deserialize_any(byte_reader.read_to_end())
    return ret

class ByteArrayReader:
    def __init__(self, byte_array):
        self.byte_array = byte_array
        self.pointer = 0

    def read(self, length):
        buffer = self.byte_array[self.pointer: self.pointer + length]
        self.pointer += length
        return buffer

    def read_to_end(self):
        buffer = self.byte_array[self.pointer: len(self.byte_array)]
        self.pointer = len(self.byte_array)
        return buffer

    def empty(self):
        return len(self.byte_array) == self.pointer




    
def bytetoint(bytes):
    return int.from_bytes(bytes, 'big')
def bytetobool(value):
    return True if value[0] else False
def bytetofloat(bytes):
    return unpack('!f', bytes)[0]
def bytetostr(bytes):
    return bytes.decode('utf-8')
def bytetobytes(body):
    return bytearray(body)
def bytetolist(bytes):
    byte_reader = ByteArrayReader(bytes)
    ret = []
    while (not byte_reader.empty()):
        body_type = byte_reader.read(1)[0]
        body = byte_reader.read(int.from_bytes(byte_reader.read(4), byteorder='big'))
        body = typeset[body_type](body)
        ret.append(body)
    return ret
def bytetodict(bytes):
    byte_reader = ByteArrayReader(bytes)
    ret = {}
    while (not byte_reader.empty()):
        len_key = byte_reader.read(1)
        key = byte_reader.read(len_key[0])
        body_type = byte_reader.read(1)[0]
        body = byte_reader.read(int.from_bytes(byte_reader.read(4), byteorder='big'))
        body = typeset[body_type](body)
        ret[key.decode()] = body
    return ret

typeset = [None, bytetoint, bytetofloat, bytetostr, bytetolist,
                        bytetodict, bytetobool, bytetobytes]
    
def get_message_type_from_value(value):
    return MessageType(value)
