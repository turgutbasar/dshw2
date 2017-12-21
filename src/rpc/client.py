import xmlrpclib

def main():
    http = "http://"
    server_add = http+ '''addr''' + ":"+ '''str(args.port)'''+"/"
    print server_add
    global proxy
    try:
        proxy = xmlrpclib.ServerProxy(server_add)
        print ("/nConnected to Proxy")
        # the first method call
    except Exception as e:
        print e
    except KeyboardInterrupt:
        exit(0)

    def new_session(self, client_id, desired_player):
        client = self.__clienlist[client_id]
        game = {}
        session = {"session_id": self.__session_numerator, "clients": [client], "game": game,
                   "desired_player": desired_player, "score_board": dict.fromKeys([client_id])}
        self.__session_numerator += 1
        self.__sessionlist.append(session)
        return session["session_id"]

if __name__== "__main__":
        main()