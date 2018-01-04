# Imports----------------------------------------------------------------------
import threading
import logging
import SocketServer
from json import JSONEncoder
from sudoku.game import Sudoku
import pika
from json import JSONDecoder

# Logging ---------------------------------------------------------------------
logging.basicConfig(level=logging.INFO, format='%(asctime)s (%(threadName)-2s) %(message)s')
LOG = logging.getLogger()

class SessionManager():

    def __init__(self):
        self.__sessionlist = []
        self.__clientlist = []
        self.__client_numerator = 0
        self.__session_numerator = 0
	connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.__channel = connection.channel()
        self.__channel.queue_declare(queue='main_queue')
        self.__channel.exchange_declare(exchange='broadcast_exchange', exchange_type='fanout')
        self.__channel.basic_qos(prefetch_count=1)
        self.__channel.basic_consume(self.on_request, queue='main_queue')

    def on_request(self,ch, method, props, body):
    	msg = JSONDecoder().decode(body)
	params = msg["params"]

        if msg["method"] == "new_player":
            response = self.new_player(params["nickname"], params["br_ip"], params["br_port"])
    	elif msg["method"] == "new_session":
            response = self.new_session(params["client_id"], params["desired_player"])
    	elif msg["method"] == "join_session":
            response = self.join_session(params["client_id"], params["session_id"])
    	elif msg["method"] == "process_game_move":
            response = self.process_game_move(params["session_id"], params["client_id"], params["move"])
    	elif msg["method"] == "client_left_session":
            response = self.client_left_session(params["session_id"], params["client_id"])
    	elif msg["method"] == "client_left_server":
            response = self.client_left_server(params["client_id"])
    	elif msg["method"] == "get_session_list":
            response = self.get_session_list()
    	else:
	    response = JSONEncoder().encode({"response":"Message Not Being Recognized"})

    	ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     body=str(response))
    	ch.basic_ack(delivery_tag = method.delivery_tag)


    def new_player(self, nickname, br_ip, br_port):
	proxy = xmlrpclib.ServerProxy("http://" + br_ip + ":" + str(br_port) + "/")
        c = {"client_id": self.__client_numerator, "nickname":nickname, "br_proxy":proxy}
        self.__client_numerator += 1
        self.__clientlist.append(c)
        return JSONEncoder().encode({"client_id":c["client_id"]})

    def new_session(self, client_id, desired_player):
        client = self.__clientlist[client_id]
        game = Sudoku()
        session = {"session_id": self.__session_numerator, "clients": [], "game": game,
                   "desired_player": desired_player, "score_board": {}}
        self.__session_numerator += 1
        self.__sessionlist.append(session)
        return JSONEncoder().encode({"session_id":session["session_id"] })

    def join_session(self, client_id, session_id):
        session = self.__sessionlist[session_id]
        client = self.__clientlist[client_id]
        if len(session["clients"]) >= session["desired_player"]:
            return JSONEncoder().encode({ "isAvailable":False })
        session["clients"].append(client)
        session["score_board"][client_id] = 0
        if len(session["clients"]) == int(session["desired_player"]):
	    game = Sudoku()
            self.broadcast(JSONEncoder().encode({ "session":session["session_id"], "msg_type":"game_started" ,"game":[game.get_board(), game.get_puzzle()] }))
        return JSONEncoder().encode({ "isAvailable":True})

    def process_game_move(self, session_id, client_id, move):
        session = self.__sessionlist[session_id]
        game = session["game"]
        clients = session["clients"]
        score_board = session["score_board"]
	status = game.check(move["i"], move["j"], move["value"])
	point = status[0]
        score_board[client_id] += point
        if status[1]:
            self.broadcast(JSONEncoder().encode({ "session":session_id, "msg_type":"game_ended", "game":[game.get_board(), game.get_puzzle()], "scores": score_board, "winner": 0}))
        else:
            self.broadcast(JSONEncoder().encode({"session":session_id, "msg_type":"move", "game":[game.get_board(), game.get_puzzle()], "scores": score_board}))
        return JSONEncoder().encode({})

    def client_left_session(self, session_id, client_id):
        session = self.__sessionlist[session_id]
        client = self.__clientlist[client_id]
        clients = session["clients"]
        game = session["game"]
        score_board = session["score_board"]
        clients.remove(client)
		
        if len(session["clients"]) < 2:
	    # TODO : Really check winner
            self.broadcast(JSONEncoder().encode({"session":session_id, "msg_type":"game_ended", "game": game.get_puzzle(), "scores": scores, "winner": clients[0]}))
        else:
            self.broadcast(JSONEncoder().encode({"session":session_id, "msg_type":"player_left", "game": game.get_puzzle(), "scores": scores}))
        return JSONEncoder().encode({})

    def client_left_server(self, client_id):
        sessions = self.__sessionlist
        for session in sessions:
            self.client_left_session(session["session_id"], client_id)
            del session

    def get_session_list(self):
        return JSONEncoder().encode([session["session_id"] for session in self.__sessionlist])

    def serve(self):
        self.__channel.start_consuming()

    def broadcast(msg):
        self.__channel.basic_publish(exchange='broadcast_exchange', routing_key='', body=str(msg))
