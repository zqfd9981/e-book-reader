import os
from typechange.message_type import MessageType
from ExtendedSocket import ExtendedSocket

def handle(sc, parameters):
    info = parameters.split('*')
    user_name = info[0] 
    book_name = info[1] 
    n = info[2] 
    book_list = os.listdir('./server/books')
    for i in range(len(book_list)):
        book_list[i] = book_list[i].strip('.txt')
    if book_name not in book_list: 
        return
    # 修改书签
    with open('./server/bookmarks_database.txt', 'r', encoding='utf-8') as f:
        user_bookmarks_list = f.read().splitlines()     #列表，每个元素存储一行，是用户的书签信息
        for i in range(len(user_bookmarks_list)):
            user_info=user_bookmarks_list[i].split('+')     #每一行以‘+’分隔
            if(user_info[0]==user_name):
                if book_name in user_info:
                    temp=user_info.index(book_name)
                    user_info[temp+1]=str(n)
                    user_bookmarks_list[i]='+'.join(user_info)
                    break
                else:
                    user_bookmarks_list[i]=user_bookmarks_list[i]+'+'+book_name+str(n)
                    break

    with open('./server/bookmarks_database.txt', 'w', encoding='utf-8') as f:      #覆盖写
        user_bookmarks_list='\n'.join(user_bookmarks_list)+'\n'
        f.write(user_bookmarks_list)
    
    return

