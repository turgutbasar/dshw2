import xmlrpclib
from json import JSONDecoder
import threading
import SimpleXMLRPCServer
import SocketServer
import pika
import json

class Client(threading.Thread):
    def __init__(self):
        self.nickname = ""
        self.tags = []
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.callback_queue = self.channel.queue_declare(exclusive=True).method.queue
        self.message_queue = self.channel.queue_declare(exclusive=True).method.queue
        self.multicast_queue = self.channel.queue_declare(exclusive=True).method.queue
        self.broadcast_queue = self.channel.queue_declare(exclusive=True).method.queue

        self.channel.queue_bind(exchange='multicast_exchange', queue=self.multicast_queue)
        self.channel.queue_bind(exchange='broadcast_exchange', queue=self.broadcast_queue)

        self.channel.basic_consume(self.__on_callback, no_ack=True,
                                   queue=self.callback_queue)

        self.channel.basic_consume(self.__on_message, no_ack=True,
                                   queue=self.message_queue)

        self.channel.basic_consume(self.__on_message, no_ack=True,
                                   queue=self.multicast_queue)

        self.channel.basic_consume(self.__on_broadcast, no_ack=True,
                                   queue=self.broadcast_queue)
        threading.Thread.__init__(self)


    def __on_broadcast(self, ch, method, props, body):
        response = json.loads(body)
        if self.nickname == "":
            return
        if response["response"] == NEW_USER_APPEARED and self.nickname:
            print(" [BC] New User Connected::" + str(response["params"][0]))
        elif response["response"] == USER_DISCONNECTED and response["params"][0] != self.nickname:
            print(" [BC] User Disconnected::" + str(response["params"][0]))
        elif response["response"] == ROOM_ENDED:
            print(" [BC] Room is closed because of being empty::" + str(response["params"][0]))

    def call(self, n):
        self.call_back_response = None
        self.channel.basic_publish(exchange='',
                                   routing_key='main_queue',
                                   properties=pika.BasicProperties(
                                       reply_to=self.callback_queue
                                   ),
                                   body=str(n))

    def run(self):
        self.channel.start_consuming()


class RPCGameClient():
    class SimpleThreadedXMLRPCServer(SocketServer.ThreadingMixIn, SimpleXMLRPCServer.SimpleXMLRPCServer):
        pass

    class BroadcastReceiver(threading.Thread):

        def __init__(self, callback, ip, port):
            self.__callback = callback
            self.__ip = ip
            self.__port = port
            threading.Thread.__init__(self)

        def on_broadcast(self, msg):
            msg = JSONDecoder().decode(msg)
            self.__callback(msg)
            return 0

        def run(self):
            server = RPCGameClient.SimpleThreadedXMLRPCServer((self.__ip, self.__port))
            server.register_instance(self)
            server.serve_forever()

    def __init__(self, brcst_server_address, brcst_server_port, brcst_callback):
        self.client = Client()
        self.__broadcast_receiver = RPCGameClient.BroadcastReceiver(brcst_callback, brcst_server_address,
                                                                    brcst_server_port)
        self.__broadcast_receiver.setDaemon(True)
        self.__broadcast_receiver.start()

    def new_player(self, nickname):
        try:
            if nickname is not None:
                self.__client_id = self.client.call(JSONDecoder().decode({"method":"new_player", "params":nickname})
                return {}
        except Exception as e:
            return {'error': e}

    def new_session(self, desired_player):
        try:
            return JSONDecoder().decode(self.__proxy.new_session(self.__client_id, desired_player))["session_id"]
        except Exception as e:
            return {'error': e}

    def join_session(self, session_id):
        try:
            status = JSONDecoder().decode(self.__proxy.join_session(self.__client_id, session_id))
            if status["isAvailable"]:
                self.__session_id = session_id
                self.__broadcast_receiver.session_id = session_id
            return status
        except Exception as e:
            print(e)
            return {'error': e}

    def process_game_move(self, move):
        try:
            JSONDecoder().decode(self.__proxy.process_game_move(self.__session_id, self.__client_id, move))
            return {}
        except Exception as e:
            print(e)
            return {'error': e}

    def client_left_session(self):
        try:
            JSONDecoder().decode(self.__proxy.client_left_session(self.__session_id, self.__client_id))
            self.__session_id = None
            self.__broadcast_receiver.session_id = None
            return {}
        except Exception as e:
            return {'error': e}

    '''def client_left_server(proxy, client_id):
        try:
            status = JSONDecoder().decode(proxy.client_left_server(client_id))
            return status
        except Exception as e:
            return {'error': e}'''

    def get_session_list(self):
        try:
            return JSONDecoder().decode(self.__proxy.get_session_list())
        except Exception as e:
            return {'error': e}
