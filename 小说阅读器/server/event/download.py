import os
from typechange.message_type import MessageType
from ExtendedSocket import ExtendedSocket

def handle(sc, parameters):
    book_list = os.listdir('./server/books')
    book_total=len(book_list)
    for i in range(book_total):
        book_list[i] = book_list[i].strip('.txt')
    if parameters not in book_list: # 如果这本书不在书籍列表里
        sc.send_message(MessageType.no_book)
        return
    file_path='./server/books/'+parameters+'.txt'
    book_file_size=os.path.getsize(file_path)
    sc.send_message(MessageType.file_size,book_file_size)
    with open(file_path,'rb') as f:
        while True:
            data=f.read(1024)
            if data=='':
                break
            else :
                sc.send(data)
    return


