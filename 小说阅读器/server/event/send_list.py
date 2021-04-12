import os
from typechange.message_type import MessageType
from ExtendedSocket import ExtendedSocket

def handle(sc, parameters):
    book_list = os.listdir('./server/books')
    book_total=len(book_list)
    for i in range(book_total):
        book_list[i] = book_list[i].strip('.txt')
    sc.send_message(MessageType.book_list, book_list)
    print('Send successfully!')
    return