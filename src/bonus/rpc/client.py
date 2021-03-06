from json import JSONEncoder,JSONDecoder
import threading
import pika

class Client(threading.Thread):

    def __init__(self, callback):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.callback_queue = self.channel.queue_declare(exclusive=True).method.queue
        #self.broadcast_queue = self.channel.queue_declare(exclusive=True).method.queue
        #self.__callback = callback
        #self.channel.queue_bind(exchange='broadcast_exchange', queue=self.broadcast_queue)

        #self.channel.basic_consume(self.__on_broadcast, no_ack=True,
        #                           queue=self.broadcast_queue)
        threading.Thread.__init__(self)


    def __on_broadcast(self, ch, method, props, body):
        msg = JSONDecoder().decode(body)
        self.__callback(msg)

    def call(self, n):
        self.call_back_response = None
        self.channel.basic_publish(exchange='',
                                   routing_key='main_queue',
                                   properties=pika.BasicProperties(
                                       reply_to=self.callback_queue
                                   ),
                                   body=str(n))
	while self.call_back_response is None:
            self.connection.process_data_events()
        return int(self.call_back_response)

    def run(self):
        self.channel.start_consuming()

class RPCGameClient():

    def __init__(self, brcst_callback):
        self.client = Client(brcst_callback)
        self.client.setDaemon(True)
        self.client.start()

    def new_player(self, nickname):
        try:
            if nickname is not None:
                self.__client_id = self.client.call(JSONEncoder().encode({"method":"new_player", "params":{ "nickname":nickname }}))
                return {}
        except Exception as e:
            return {'error': e}

    def new_session(self, desired_player):
        try:
            return self.client.call(JSONDecoder().decode({"method": "new_session","params": {"client_id": self.__client_id, "desired_player": desired_player}}))
        except Exception as e:
            return {'error': e}

    def join_session(self, session_id):
        try:
            status = self.client.call(JSONEncoder().encode({"method":"join_session", "params":{"client_id": self.__client_id,"session_id": session_id}}))

            if status["isAvailable"]:
                self.__session_id = session_id
                self.__broadcast_receiver.session_id = session_id
            return status
        except Exception as e:
            print(e)
            return {'error': e}

    def process_game_move(self, move):
        try:
            self.client.call(JSONEncoder().encode({"method": "process_game_move" , "params": {"session_id": self.__session_id, "client_id": self.__client_id, "move": move}}))
            return {}
        except Exception as e:
            print(e)
            return {'error': e}

    def client_left_session(self):
        try:
            self.client.call(JSONEncoder().encode({"method": "client_left_session","params": {"session_id": self.__session_id, "client_id": self.__client_id}}))
            self.__session_id = None
            self.__broadcast_receiver.session_id = None
            return {}
        except Exception as e:
            return {'error': e}

    def client_left_server(self, client_id):
        try:
            return self.client.call(JSONEncoder().encode({"method": "client_left_server","params": {"client_id": self.__client_id}}))
        except Exception as e:
            return {'error': e}

    def get_session_list(self):
        try:
            return self.client.call(JSONEncoder().encode({"method": "get_session_list", "params": {}}))
        except Exception as e:
            return {'error': e}
