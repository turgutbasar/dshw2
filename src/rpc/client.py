import xmlrpclib

import client.py as cl


def new_player(nickname, client_address, client_port):
    server_add = "http://" + client_address + ":" + client_port + "/"
    try:
        proxy = xmlrpclib.ServerProxy(server_add)
        global client_id
        client_id = proxy.new_player(nickname)
    except Exception as e:
        cl.error_message(e)
    except KeyboardInterrupt:
        exit(0)

def new_session():
    pass

def join_session():
    pass
    
def is_seesion_ready():
    pass

def process_game_move():
    pass

def client_left_session():
    pass

def cient_left_server():
    pass

def get_client_list():
    pass

