import server.event.login
import server.event.register
import server.event.send_list
import server.event.download
import server.event.reading
import server.event.read_one_page
import server.event.update_bookmark
from typechange.message_type import MessageType

event_handler_map = {
    MessageType.login: login,
    MessageType.register: register,    
    MessageType.require_list: send_list,
    MessageType.download: download,
    MessageType.reading: reading,
    MessageType.require_page: read_one_page,
    MessageType.update_bookmark: update_bookmark,
}

def handle_event(sc, event_type, parameters):
    event_handler_map[event_type].handle(sc, parameters)