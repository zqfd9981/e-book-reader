import os
from typechange.message_type import MessageType
from ExtendedSocket import ExtendedSocket

def read_given_page(sc, book_path, page_num):
    with open(book_path, 'r', encoding='utf-8') as f:
        if f.readline() == 'C\n':
            page_words = 1000
        else:
            page_words =2500
        begin=0
        page=0
        line = f.readline()
        while page <= page_num:
            content = ''
            if line:
                content += line
                line = f.readline()
                while line:
                    if line[0] == '#':
                        break
                    content += line
                    line = f.readline()
            page_read=len(content)//page_words
            if page+page_read< page_num: 
                page +=(page_read+1)
                continue
            elif page+page_read == page_num: 
                begin = page_words *page_read
                page += (page_read+1)
            else: 
                begin = page_words * (page_num - page)
                page = page_num
                break
        sc.send_message(MessageType.send_page, content[begin: begin+page_words])
    return

def handle(sc, parameters):
    book = parameters.split('*')
    book_name = book[0] 
    page_num = int(book[1]) 
    book_list = os.listdir('./server/books')
    for i in range(len(book_list)):
        book_list[i] = book_list[i].strip('.txt')
    if book_name not in book_list: # 如果这本书不在书籍列表里
        sc.send_message(MessageType.no_book)
        return

    read_given_page(sc, './server/books/' + book_name + '.txt', page_num)

    return