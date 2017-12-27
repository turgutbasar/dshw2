# Imports----------------------------------------------------------------------
from multiprocessing import Queue
import threading
import logging
import SocketServer
from json import JSONEncoder
import SimpleXMLRPCServer


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s (%(threadName)-2s) %(message)s')
LOG = logging.getLogger()

client_numerator = 0
session_numerator = 0

class SimpleThreadedXMLRPCServer(SocketServer.ThreadingMixIn, SimpleXMLRPCServer.SimpleXMLRPCServer):
    pass

# Class Impl ------------------------------------------------------------------
class SessionManager():
    def __init__(self):
        self.__sessionlist = []
        self.__clientlist = []
        self.__client_numerator = 0
        self.__session_numerator = 0

    def new_player(self, nickname):
        c = {"client_id": self.__client_numerator, "nickname":nickname}
        self.__client_numerator += 1
        self.__clientlist.append(c)
        return JSONEncoder().encode({ "client_id":c["client_id"] })

    def new_session(self, client_id, desired_player):
        client = self.__clientlist[client_id]
        game = {}
        session = {"session_id": self.__session_numerator, "clients": [client], "game": game,
                   "desired_player": desired_player, "score_board": dict.fromKeys([client_id])}
        self.__session_numerator += 1
        self.__sessionlist.append(session)
        return JSONEncoder().encode({ "session_id":session["session_id"] })

    def join_session(self, client_id, session_id):
        session = self.__sessionlist[session_id]
        client = self.__clientlist[client_id]
        if len(session["clients"]) >= session["desired_player"]:
            JSONEncoder().encode({ "isAvailable":False })
        else:
            session["clients"].append(client)
            session["score_board"][client_id] = 0
            if len(session["clients"]) == session["desired_player"]:
				# Broadcasting
				return JSONEncoder().encode({ "isAvailable":True ,"game":session["game"] })
            else:
				return JSONEncoder().encode({ "isAvailable":True })

    def process_game_move(self, session_id, client_id, move):
        session = self.__sessionlist[session_id]
        game = session["game"]
        clients = session["clients"]
        scores = session["scores"]
        score_board = session["score_board"]
        if game.check(move["i"], move["j"], move["value"]):
            score_board[client_id] += 1
        else:
            score_board[client_id] -= 1
		# Broadcasting
        if game.isEnded():
            return JSONEncoder().encode({"game": game, "isEnded": True, "scores": scores, "winner": 0})
        else:
            return JSONEncoder().encode({"game": game, "isEnded": False, "scores": scores})

    def client_left_session(self, session_id, client_id):
        session = self.__sessionlist[session_id]
        client = self.__clientlist[client_id]
        clients = session["clients"]
        game = session["game"]
        scores = session["scores"]
        clients.remove(client)
        # Checks if game ended
		# Broadcasting
        if len(session["clients"]) < 2:
            return JSONEncoder().encode({"game": game, "isEnded": True, "scores": scores, "winner": session["clients"][0]})
        else:
            return JSONEncoder().encode({"game": game, "isEnded": False, "scores": scores})

    def client_left_server(self, client_id):
        session=self.__sessionlist[session_id]
        for session_id in session:
            self.client_left_session(session_id, client_id)
            del session_id
            #Broadcast

    def get_session_list(self):
        return JSONEncoder().encode(self.__sessionlist)

    def serve(self, ip, port):
        server = SimpleThreadedXMLRPCServer((ip, port))
        server.register_instance(self) # register your distant Object here
        server.serve_forever()
