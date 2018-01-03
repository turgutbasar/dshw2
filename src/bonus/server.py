# Imports ---------------------------------------------------------------------
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
    try:
        SessionManager().serve()
    except KeyboardInterrupt:
        LOG.info('Terminating server ...')
