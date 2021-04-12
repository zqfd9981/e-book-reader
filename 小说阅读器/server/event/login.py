from typechange.message_type import MessageType
from ExtendedSocket import ExtendedSocket

def handle(sc, parameters):
    with open('./server/users.txt', 'r', encoding='utf-8') as f:
        usernames=f.read().splitlines()
        for user in usernames:
            user = user.split('|')
            if parameters[0] == user[0] and parameters[1] == user[1]: # 用户名和密码正确
                sc.send_message(MessageType.login_successful)
                print('Login successfully')
                return

    sc.send_message(MessageType.login_failed)
    return
