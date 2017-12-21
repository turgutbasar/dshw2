# Imports----------------------------------------------------------------------
from exceptions import Exception
# TCP related constants -------------------------------------------------------
#
DEFAULT_SERVER_PORT = 7777
DEFAULT_SERVER_INET_ADDR = '127.0.0.1'
#
# protocol constants ----------------------------------------------------------
# Field separator for sending multiple values ---------------------------------
__MSG_FIELD_SEP = ':'
# Requests --------------------------------------------------------------------
__REQ_REGISTRATION = '1'
__REQ_NEW_SESSION = '2'
__REQ_JOIN_EXISTING = '3'
__REQ_BOARD_CHANGE = '4'
__REQ_CLIENT_LEFT = '5'

__CTR_MSGS = { __REQ_REGISTRATION:'Registration', __REQ_NEW_SESSION:'New session', __REQ_JOIN_EXISTING:'Join existing', __REQ_BOARD_CHANGE:'Game board change'
             }
# Responses--------------------------------------------------------------------
__RSP_OK = '0'
__RSP_BADFORMAT = '1'
__RSP_UNKNCONTROL = '3'
__RSP_ERRTRANSM = '4'
__RSP_CANT_CONNECT = '5'
__RSP_SESSION_LIST = '6'
__RSP_BOARD = '7'
__RSP_SESSION_IS_FULL = '8'
__RSP_ENDGAME = '9'
__RSP_BOARDUPDATE = '10'
__ERR_MSGS = { __RSP_OK:'No Error',
               __RSP_BADFORMAT:'Malformed message',
               __RSP_UNKNCONTROL:'Unknown control code',
               __RSP_ERRTRANSM:'Transmission Error',
               __RSP_CANT_CONNECT:'Can\'t connect to server',
               __RSP_SESSION_LIST:'Session list',
               __RSP_BOARD:'Game board',
               __RSP_SESSION_IS_FULL:'Session is full'
              }