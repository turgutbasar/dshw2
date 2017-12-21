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

if __name__== "__main__":
        main()