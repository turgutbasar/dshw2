import xmlrpclib

import  src.client as cl

def new_player(nickname, server_address, server_port):
    try:
        if nickname is not None and server_address != "" and server_port != "":
            server_add = "http://" + server_address + ":" + server_port + "/"
            proxy = xmlrpclib.ServerProxy(server_add)
            client_id = proxy.new_player(nickname)
            return proxy, client_id
    except Exception as e:
        cl.error_message(e)

def new_session(proxy, client_id, desired_player):
    try:
        session_id = proxy.new_session(client_id, desired_player)
        return session_id
    except Exception as e:
        cl.error_message(e)

def join_session(proxy, client_id, session_id):
    try:
        #success on joining
        status = proxy.join_session(client_id, session_id)
        return status
    except Exception as e:
        cl.error_message(e)

def is_session_ready(proxy, session_id):
    try:
        session = proxy.is_session_ready(session_id)
        return session
    except Exception as e:
        cl.error_message(e)

def process_game_move(proxy, session_id, client_id, move):
    try:
        game = proxy.process_game_move(session_id, client_id, move)
        return game
    except Exception as e:
        cl.error_message(e)

def client_left_session(proxy, session_id, client_id):
    try:
        game = proxy.client_left_session(session_id, client_id)
        return game
    except Exception as e:
        cl.error_message(e)

def client_left_server(proxy, client_id):
    try:
        game = proxy.client_left_server(client_id)
        return game
    except Exception as e:
        cl.error_message(e)

def get_client_id(proxy, client_address):
    try:
        client_id = proxy.get_client_id(client_address)
        return client_id
    except Exception as e:
        cl.error_message(e)

def get_session_list(proxy):
    try:
        #deqiqleshdir
        session_list = proxy.get_session_list()
        return session_list
    except Exception as e:
        cl.error_message(e)
