import xmlrpclib
from json import JSONDecoder
import threading
import SimpleXMLRPCServer
import SocketServer


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

    def __init__(self, server_address, server_port, brcst_server_address, brcst_server_port, brcst_callback):
        self.__proxy = xmlrpclib.ServerProxy("http://" + server_address + ":" + server_port + "/")
        self.__br_ip = brcst_server_address
        self.__br_port = brcst_server_port
        self.__broadcast_receiver = RPCGameClient.BroadcastReceiver(brcst_callback, brcst_server_address,
                                                                    brcst_server_port)
        self.__broadcast_receiver.setDaemon(True)
        self.__broadcast_receiver.start()

    def new_player(self, nickname):
        try:
            if nickname is not None:
                self.__client_id = \
                JSONDecoder().decode(self.__proxy.new_player(nickname, self.__br_ip, self.__br_port))["client_id"]
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
