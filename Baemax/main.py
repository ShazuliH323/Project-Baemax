from website import create_web
from flask_socketio import join_room, leave_room , send, SocketIO 
import random

from string import ascii_uppercase


web = create_web()

if __name__ == '__main__':
    
    my_list = list(web)
    my_list[0].run(debug=True)
    my_list[1].run(debug=True)
    
    socketio.run(web, debug=True)
    
