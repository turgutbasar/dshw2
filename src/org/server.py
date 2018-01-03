# Imports ---------------------------------------------------------------------
from argparse import ArgumentParser
from rpc.common import DEFAULT_SERVER_RPC_ADDR, DEFAULT_SERVER_RPC_PORT
from rpc.session_manager import SessionManager
from os.path import abspath, sep
from sys import path,argv
import logging

# Logging ---------------------------------------------------------------------
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s (%(threadName)-2s) %(message)s')
LOG = logging.getLogger()

# Main method -----------------------------------------------------------------
if __name__ == '__main__':
    # Find the script absolute path, cut the working directory
    a_path = sep.join(abspath(argv[0]).split(sep)[:-1])
    # Append script working directory into PYTHONPATH
    path.append(a_path)
    # Parsing arguments
    parser = ArgumentParser(description="Sudoku Game Server of DS Homework2",
                            version = "RPC Version")
    parser.add_argument('-l','--listenaddr', \
                        help='RPC end point listening address, '\
                        'defaults to %s' % DEFAULT_SERVER_RPC_ADDR, \
                        default=DEFAULT_SERVER_RPC_ADDR)
    parser.add_argument('-p','--listenport', \
                        help='RPC end point listening port, '\
                        'defaults to %d' % DEFAULT_SERVER_RPC_PORT, \
                        default=DEFAULT_SERVER_RPC_PORT)
    args = parser.parse_args()
    try:
        SessionManager().serve(args.listenaddr, args.listenport)
    except KeyboardInterrupt:
        LOG.info('Terminating server ...')
