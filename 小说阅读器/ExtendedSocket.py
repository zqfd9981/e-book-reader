import math
import os
import socket
import struct

from typechange.typetobyte import *
from typechange.typetobyte import serialize_message
from typechange.message_type import MessageType
from typechange.bytetotype import deserialize_message


class ExtendedSocket:

    def __init__(self, socket):
        self.socket = socket
        return
 
    def send_message(self, message_type, parameters=None):
        data_buffer = serialize_message(message_type, parameters)
        length_of_message = len(data_buffer)
        self.socket.send(struct.pack('!L', length_of_message) + data_buffer)  
        return

    def recv_message(self):
        bytes_to_receive = 0
        bytes_received = 0
        while True:
            if bytes_to_receive == 0 and bytes_received == 0:
                conn_ok = True
                first_4_bytes = ''
                try:
                    first_4_bytes = self.socket.recv(4) # 接收4bytes，内容是message的长度
                except ConnectionError:
                    conn_ok = False
                if first_4_bytes == "" or len(first_4_bytes) < 4:
                    conn_ok = False
                if not conn_ok:
                    print('连接失败！')
                    return False
                data_buffer = bytes()
                bytes_to_receive = struct.unpack('!L', first_4_bytes)[0]

            buffer = self.socket.recv(bytes_to_receive - bytes_received)
            data_buffer += buffer
            bytes_received += len(buffer)

            if bytes_received == bytes_to_receive:       
                message = deserialize_message(data_buffer)
                return message

    def send_file(self, file_path):

        self.send_message(MessageType.file_size, os.stat(file_path).st_size)
        
        with open(file_path,'rb') as f: 
            while True:
                filedata = f.read(1024) 
                if not filedata:
                    break
                self.socket.send(filedata)       
        print('已发送文件')
        return

    def recv_file(self, file_path):
        """客户端从服务器接收文件"""
        message = self.recv_message()
        if message['type'] == MessageType.no_book:
            print('查无此书！')
            return
        if message['type'] is not MessageType.file_size:
            print('未能获取文件大小，传输失败！')
            return
        
        filesize = message['parameters'] # 要传输的文件大小
        try:
            with open(file_path,'wb') as f: # 二进制打开文件用于写入
                while True:
                    buffer = self.socket.recv(1024)
                    if not buffer:
                        break    
                f.write(buffer)
        except Exception as e:
            print (e)
        return

    def close(self):
        self.socket.close()


def establish_secure_channel_to_server():

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    HOST='127.0.0.1'
    Port=6543

    s.connect((HOST,Port)) # 建立连接

    sc = ExtendedSocket(s)
    print('安全通道建立成功')

    return sc


def accept_client_to_secure_channel(socket):
    """
    服务器建立安全通道
    """
    conn, addr = socket.accept() # 这里仍然使用socket接收
    sc = ExtendedSocket(conn)
    print('安全通道建立成功')
    return sc