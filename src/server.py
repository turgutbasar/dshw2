# Imports----------------------------------------------------------------------
from argparse import ArgumentParser # Parsing command line arguments
from sys import path,argv
from os.path import abspath, sep
from tcp.server.main import __info, ___VER, server_main
from tcp.common import DEFAULT_SERVER_INET_ADDR, DEFAULT_SERVER_PORT

import time
import logging
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s (%(threadName)-2s) %(message)s')
LOG = logging.getLogger()

# Main method -----------------------------------------------------------------
if __name__ == '__main__':
    # Find the script absolute path, cut the working directory
    a_path = sep.join(abspath(argv[0]).split(sep)[:-1])
    # Append script working directory into PYTHONPATH
    path.append(a_path)
    # Parsing arguments
    parser = ArgumentParser(description=__info(),
                            version = ___VER)
    parser.add_argument('-l','--listenaddr', \
                        help='Bind server socket to INET address, '\
                        'defaults to %s' % DEFAULT_SERVER_INET_ADDR, \
                        default=DEFAULT_SERVER_INET_ADDR)
    parser.add_argument('-p','--listenport', \
                        help='Bind server socket to UDP port, '\
                        'defaults to %d' % DEFAULT_SERVER_PORT, \
                        default=DEFAULT_SERVER_PORT)
    args = parser.parse_args()
    try:
		# Starting server
		LOG.info('%s version %s started ...' % (___NAME, ___VER))
		LOG.info('Using %s version %s' % ( protocol.___NAME, protocol.___VER))
			
		# Declaring TCP socket
		__server_socket = socket(AF_INET,SOCK_STREAM)
		LOG.debug('Server socket created, descriptor %d' % __server_socket.fileno())
		# Bind TCP Socket
		try:
			__server_socket.bind((args.listenaddr,int(args.listenport)))
		except soc_error as e:
			LOG.error('Can\'t start sudoku game server, error : %s' % str(e))
			exit(1)

		LOG.debug('Server socket bound on %s:%d' % __server_socket.getsockname())

		# Put TCP socket into listening state
		__server_socket.listen(__DEFAULT_SERVER_TCP_CLIENTS_QUEUE)
		LOG.info('Accepting requests on TCP %s:%d' % __server_socket.getsockname())

		# Client List
		client_list = []

		session_list = []

		worker_list = []

		client_numerator = 0
		

		# Serve forever
		while 1:
			try:
				LOG.debug('Awaiting new client connections ...')
				# Accept client's connection store the client socket into
				# client_socket and client address into source
				client_socket,source = __server_socket.accept()
				LOG.debug('New client connected from %s:%d' % source)
			
				client_numerator += 1
				client = {"client_id": client_numerator, "client_socket": client_socket, "addr": source}
				client_list.append(client)

				# Handles incoming connection requests, creates new worker, asigns client to worker
				# Worker need to handle protocol, messaging.
				def close_callback(e, c):
					LOG.debug(e);
					return;

				worker = ProtocolWorker(client, session_list, close_callback)

				worker_list.append(worker)

				worker.run()

			except KeyboardInterrupt as e:
				LOG.info('Terminating socket communication ...')
				break

		# If we were interrupted, make sure client socket is also closed
		for client in client_list:
			if client["client_socket"] != None:
				__disconnect_client(client["client_socket"])

		# Close server socket
		__server_socket.close()
		LOG.debug('Server socket closed')
		raise KeyboardInterrupt("")

    except KeyboardInterrupt:
	LOG.info('Terminating server ...')