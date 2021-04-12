import os
import math
from typechange.message_type import MessageType
from ExtendedSocket import ExtendedSocket
from server.event.read_one_page import read_given_page

def handle(sc, parameters):
    user = parameters.split('*')
    Username = user[0] 
    book_name = user[1] 

    book_list = os.listdir('./server/books')
    for i in range(len(book_list)):
        book_list[i] = book_list[i].strip('.txt')
    if book_name not in book_list:
        sc.send_message(MessageType.no_book)
        return

    # 查找书签
    page_num = 0 # 初始化书签为0
    with open('./server/bookmarks_database.txt', 'r', encoding='utf-8') as f:
        user_list = f.read().splitlines() 
        for user in user_list:
            user_info=user.split('+')
            if user_info[0]==Username:
                if book_name in user_info:
                    temp=user_info.index(book_name)
                    page_num=int(user_info[temp+1])
                    break
                else:
                    page_num=0
                    break
        sc.send_message(MessageType.page_num, page_num) 
    total_page = 0
    chapter = []
    chapter.append(['目录', 0])
    i = 1
    with open('./server/books/' + book_name + '.txt', 'r', encoding='utf-8') as f:
        if f.readline() == 'C\n':
            page_words =1000
        else:
            page_words =2500
        line = f.readline()
        while line:
            s = ''
            s += line
            line = f.readline()
            while line:
                if line[0] == '#':
                    break
                s += line
                line = f.readline()
            total_page +=len(s)//page_words+1
            chapter.append([line[1:-1], total_page])
    sc.send_message(MessageType.total_page, total_page-1) # 发送总页数
    sc.send_message(MessageType.send_chapter, chapter[:-1]) # 发送章数列表

    read_given_page(sc, './server/books/' + book_name + '.txt', page_num)
    return