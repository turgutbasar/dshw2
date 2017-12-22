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
        self.__client_mapping = {}
        self.__client_numerator = 0
        self.__session_numerator = 0

    def new_player(self, nickname, socket, addr):
        c = {"client_id": self.__client_numerator, "client_socket": socket, "addr": addr,"nickname":nickname}
        self.__client_numerator += 1
        self.__clientlist.append(c)
        self.__client_mapping[str(addr[0]) + ":" + str(addr[1])] = c["client_id"]
        return c["client_id"]

    def new_session(self, client_id, desired_player):
        client = self.__clienlist[client_id]
        game = {}
        session = {"session_id": self.__session_numerator, "clients": [client], "game": game,
                   "desired_player": desired_player, "score_board": dict.fromKeys([client_id])}
        self.__session_numerator += 1
        self.__sessionlist.append(session)
        return session["session_id"]

    def join_session(self, client_id, session_id):
        session = self.__sessionlist[session_id]
        client = self.__clientlist[client_id]
        if len(session["clients"]) >= session["desired_player"]:
            return False
        else:
            session["clients"].append(client)
            session["score_board"][client_id] = 0
            return True

    def is_session_ready(self, session_id):
        session = self.__sessionlist[session_id]
        if len(session["clients"]) >= session["desired_player"]:
            return (session["clients"], JSONEncoder().encode(session["game"]),)
        else:
            return False

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
        if game.isEnded():
            return (
            True, clients, JSONEncoder().encode({"game": game, "isEnded": True, "scores": scores, "winner": 0}),)
        else:
            return (False, clients, JSONEncoder().encode({"game": game, "isEnded": False, "scores": scores}),)

    def client_left_session(self, session_id, client_id):
        session = self.__sessionlist[session_id]
        client = self.__clientlist[client_id]
        clients = session["clients"]
        game = session["game"]
        scores = session["scores"]
        clients.remove(client)
        # Checks if game ended
        if len(session["clients"]) < 2:
            return (True, clients, JSONEncoder().encode(
                {"game": game, "isEnded": True, "scores": scores, "winner": session["clients"][0]}),)
        else:
            return (False, clients, JSONEncoder().encode({"game": game, "isEnded": True, "scores": scores}),)

    def client_left_server(self, client_id):
        # TODO : check every session to clean user and return ended games
        session=self.__sessionlist[session_id]
        for session_id in session:
            del session_id
            #Broadcast
        return JSONEncoder().encode({"game": game, "isEnded": True, "scores": scores})


    def get_client_id(self, addr):

        return self.__client_mapping[str(addr[0]) + ":" + str(addr[1])]



    def get_session_list(self):
        return JSONEncoder().encode(self.__sessionlist)
      
    def serve(self, ip, port):
<<<<<<< HEAD
       server = SimpleThreadedXMLRPCServer((ip, port))
       server.register_instance(self) # register your distant Object here
       server.serve_forever()
=======
        server = SimpleThreadedXMLRPCServer((ip, port))
        server.register_instance(self) # register your distant Object here
        server.serve_forever()
>>>>>>> 39ed5cec4ae3fdb2c600d8e7a8d8cab1998b07e6
