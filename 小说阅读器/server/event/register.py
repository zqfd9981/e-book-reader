from typechange.message_type import MessageType
from typechange.typetobyte import serialize_message
from ExtendedSocket import ExtendedSocket

def handle(sc, parameters):
    with open('./server/users.txt', 'r', encoding='utf-8') as f:
        usernames=f.read().splitlines()
        for user in usernames:
            user=user.split('|')
            if parameters[0]==user[0] or parameters[1]==user[1]:
                print('Username has been occupied!')
                sc.send_message(MessageType.username_occupied)
                return
    with open('./server/users.txt', 'a+', encoding='utf-8') as f:
        f.write(parameters[0]+'|'+parameters[1]+'\n')
    sc.send_message(MessageType.register_successful)
    return
