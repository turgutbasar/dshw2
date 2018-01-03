# Imports----------------------------------------------------------------------
from argparse import ArgumentParser
from rpc.common import DEFAULT_CLIENT_RPC_BRDCST_ADDR, DEFAULT_CLIENT_RPC_BRDCST_PORT
from os.path import abspath, sep
from sys import path,argv
from gui.gui import GUI
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
    parser = ArgumentParser(description="Sudoku Game Client of DS Homework2",
                            version = "RPC Version")
    parser.add_argument('-l','--listenaddr', \
                        help='RPC broadcast recv address, '\
                        'defaults to %s' % DEFAULT_CLIENT_RPC_BRDCST_ADDR, \
                        default=DEFAULT_CLIENT_RPC_BRDCST_ADDR)
    parser.add_argument('-p','--listenport', \
                        help='RPC broadcast recv port, '\
                        'defaults to %d' % DEFAULT_CLIENT_RPC_BRDCST_PORT, \
                        default=DEFAULT_CLIENT_RPC_BRDCST_PORT)
    args = parser.parse_args()

    try:
        GUI(args.listenaddr, args.listenport).gui_start()
    except KeyboardInterrupt:
        LOG.info('Terminating client ...')
