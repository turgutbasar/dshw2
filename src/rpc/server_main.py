#!/usr/bin/python

from tcp.server.protocol import __disconnect_client
from tcp.server.protocol_worker import ProtocolWorker
from tcp.server.session_manager import SessionManager
'''
Sudoku Game Server (TCP)
Created on Nov 5, 2017

@author: basar
'''
# Setup Python logging ------------------ -------------------------------------
import logging
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s (%(threadName)-2s) %(message)s')
LOG = logging.getLogger()
# Imports ---------------------------------------------------------------------
from tcp.server import protocol
from tcp.common import tcp_receive, tcp_send
from socket import socket, AF_INET, SOCK_STREAM
from socket import error as soc_error
from sys import exit
# Constants -------------------------------------------------------------------
___NAME = 'Sudoku Game Server'
___VER = '0.1.0.0'
___DESC = 'Sudoku Game Server (TCP version)'
___BUILT = '2017-11-5'
___VENDOR = 'Copyright (c) 2017 DSLab'
# -----------------------------------------------------------------------------
# How many clients may there be awaiting to get connection if the server is
# currently busy processing the other request
__DEFAULT_SERVER_TCP_CLIENTS_QUEUE = 10
# Private methods -------------------------------------------------------------
def __info():
    return '%s version %s (%s) %s' % (___NAME, ___VER, ___BUILT, ___VENDOR)
