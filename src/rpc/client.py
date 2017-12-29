import xmlrpclib

import src.client as cl
from json import JSONDecoder
import pika

class BroadcastReceiver(threading.Thread):
    def __init__(self, callback):
	self.nickname = ""
	self.tags = []
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
	self.broadcast_queue = self.channel.queue_declare(exclusive=True).method.queue

	self.channel.queue_bind(exchange='broadcast_exchange', queue=self.broadcast_queue)


	self.channel.basic_consume(callback, no_ack=True,
                                   queue=self.broadcast_queue)
	threading.Thread.__init__(self)

    def run(self):
	self.channel.start_consuming()

def new_broadcast_receiver(callback):
    return BroadcastReceiver(callback)

def new_player(nickname, server_address, server_port):
    try:
        if nickname is not None and server_address != "" and server_port != "":
            server_add = "http://" + server_address + ":" + server_port + "/"
            proxy = xmlrpclib.ServerProxy(server_add)
            client_id = JSONDecoder().decode(proxy.new_player(nickname))
            return proxy, client_id
    except Exception as e:
        cl.error_message(e)

def new_session(proxy, client_id, desired_player):
    try:
        session_id = JSONDecoder().decode(proxy.new_session(client_id, desired_player))
        return session_id
    except Exception as e:
        cl.error_message(e)

#changed
def join_session(proxy, client_id, session_id):
    try:
        #success on joining
        game_join = JSONDecoder().decode(proxy.join_session(client_id, session_id))
        return game_join
    except Exception as e:
        cl.error_message(e)

def is_session_ready(proxy, session_id):
    try:
        session = JSONDecoder().decode(proxy.is_session_ready(session_id))
        return session
    except Exception as e:
        cl.error_message(e)

#changed: return dict
def process_game_move(proxy, session_id, client_id, move):
    try:
        game = JSONDecoder().decode(proxy.process_game_move(session_id, client_id, move))
        return game
    except Exception as e:
        cl.error_message(e)


#changed: return dict
def client_left_session(proxy, session_id, client_id):
    try:
        game = JSONDecoder().decode(proxy.client_left_session(session_id, client_id))
        return game
    except Exception as e:
        cl.error_message(e)

#changed:default return True
def client_left_server(proxy, client_id):
    try:
        status = JSONDecoder().decode(proxy.client_left_server(client_id))
        return status
    except Exception as e:
        cl.error_message(e)

def get_client_id(proxy, client_address):
    try:
        client_id = JSONDecoder().decode(proxy.get_client_id(client_address))
        return client_id
    except Exception as e:
        cl.error_message(e)

def get_session_list(proxy):
    try:
        #deqiqleshdir
        session_list = JSONDecoder().decode(proxy.get_session_list())
        return session_list
    except Exception as e:
        cl.error_message(e)
