import enum

class MessageType(enum.IntEnum):
    login = 1
    register = 2
    require_list = 3
    download = 4
    reading = 5
    require_page = 6
    update_bookmark = 7
    login_successful = 101
    register_successful = 102
    book_list = 103
    file_size = 104
    send_page = 105
    send_chapter = 106 
    page_num = 107
    total_page = 108
    login_failed = 201 
    no_book = 202 

def _get_message_type_from_value(value):
    return MessageType(value)