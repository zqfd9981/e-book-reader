"""
类型转化函数，将'int'等类型封装转化为byte
"""
import socket
import enum
from struct import pack, unpack
from typechange.message_type import MessageType
from binascii import unhexlify

VAR_TYPE_INVERSE = {
    'int': 1,
    'float': 2,
    'str': 3,
    'list': 4,
    'dict': 5,
    'bool': 6,
    'bytearray': 7
}


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

def _serialize_int(int):
    body = long_to_bytes(int)
    return bytes([VAR_TYPE_INVERSE['int']]) + pack('!L', len(body)) + body


def _serialize_bool(value):
    body = value
    return bytes([VAR_TYPE_INVERSE['bool']]) + pack('!L', 1) + bytes([1 if value else 0])


def _serialize_float(float):
    body = pack('f', float)
    return bytes([VAR_TYPE_INVERSE['float']]) + pack('!L', len(body)) + body


def _serialize_str(str):
    body = str.encode()
    return bytes([VAR_TYPE_INVERSE['str']]) + pack('!L', len(body)) + body


def _serialize_bytes(body):
    return bytes([VAR_TYPE_INVERSE['bytearray']]) + pack('!L', len(body)) + body


def _serialize_list(list):
    body = bytearray()
    for i in range(0, len(list)):
        body += _serialize_any(list[i])
    return bytes([VAR_TYPE_INVERSE['list']]) + pack('!L', len(body)) + body


def _serialize_dict(dict):
    body = bytearray()
    for item_key, value in dict.items():
        item_body = _serialize_any(value)
        key_length = len(item_key)
        body += bytes([key_length])
        body += str.encode(item_key)
        body += item_body

    return bytes([VAR_TYPE_INVERSE['dict']]) + pack('!L', len(body)) + body


_serialize_by_type = [None, _serialize_int, _serialize_float, _serialize_str, _serialize_list, _serialize_dict,
                      _serialize_bool, _serialize_bytes]


def _serialize_any(obj):
    if obj is None:
        return bytearray([0])
    type_byte = VAR_TYPE_INVERSE[type(obj).__name__] # 首先判断是哪个类型，再调用相应的函数
    return _serialize_by_type[type_byte](obj)


def serialize_message(message_type, parameters=None):
    """将message_type和message本身转化为byte合并返回"""
    result = bytes([message_type.value])
    result += _serialize_any(parameters)
    return result