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


