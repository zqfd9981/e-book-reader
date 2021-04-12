#初始化服务器，等待客户端请求
import socket
import struct
import sys
import traceback
import select
from ExtendedSocket import ExtendedSocket
from typechange.bytetotype import deserialize_message
from typechange.message_type import MessageType
from server.event import handle_event
from pprint import pprint

def init_server():
    HOST='127.0.0.1'
    Port=6543
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
    s.bind((HOST,Port))
    s.listen(5)

    print("Server listening on " + HOST + ":" + str(Port))

    length_bytes={} 
    has_received = {}
    buffer = {}
    inputs=[s]
    while True:
        readable, writable, exceptional= select.select(inputs, [], [])

        for i in readable:
            if i == s:
                connection,addr=s.accept()
                inputs.append(connection)
                length_bytes[connection] = 0
                has_received[connection] = 0
                buffer[connection] = bytes()
                continue
            else:
                if has_received[i] == 0:
                    length_bytes[i] =struct.unpack('!L',i.recv(4))[0]
                    new_received = i.recv(length_bytes[i] - has_received[i])
                    buffer[i] += new_received  
                    has_received[i] += len(new_received)

                if has_received[i] ==length_bytes[i] and has_received[i] != 0:
                    has_received[i]=0
                    length_bytes[i]=0
                    try:
                        data = buffer[i]
                        message = deserialize_message(data)
                        extended=ExtendedSocket(i)
                        handle_event(extended, message['type'], message['parameters'])
                    except:
                        pprint(sys.exc_info())
                        traceback.print_exc(file=sys.stdout)
                        pass
                    buffer[i] = bytes()
