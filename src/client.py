# Imports----------------------------------------------------------------------
from Tkinter import *
import tkMessageBox
from gui.game_screen import SudokuApp
from rpc.client import get_session_list, new_player, new_session, join_session
from os.path import abspath, sep
from sys import path,argv

# Vars -----------------------------------------------------------------
nickname = ""
login_screen_frame = None
connect_server_screen_frame = None
multiplayer_game_screen_frame = None
new_session_screen_frame = None
sudoku_app = None
proxy = None
client_id = None
session = None

# Methods -----------------------------------------------------------------
def error_message(message):
    tkMessageBox.showerror("Error", message)

def info_message(message):
    tkMessageBox.showinfo("Info", message)

# show nickname screen
def login_screen():
    def on_select(event):
    	widget = event.widget
	global nickname    	
	nickname = widget.get(widget.curselection())
    	connect_server_screen()

    def get_nickname(tb_nick):
	global nickname
    	nickname = tb_nick.get("1.0",'end-1c')
    	if (nickname != '') and (' ' not in nickname) and len(nickname) <= 8:
            write_names = open("nicknames", "a")
            write_names.write("\n"+nickname)
            connect_server_screen()
        else:
            error_message("your nickname is not valid")

    read_names = open("nicknames", "r")
    names = read_names.read().split()
    global login_screen_frame
    login_screen_frame = Tk()
    login_screen_frame.title("Enter Nickname")
    lb_names = Listbox(login_screen_frame, selectmode='single')
    lb_names.bind('<<ListboxSelect>>', on_select)
    for n in names:
        lb_names.insert(END,n)
    lb_names.pack()
    btn_okay = Button(login_screen_frame, text="ok", command=lambda : get_nickname(tb_nick), width=20)
    btn_okay.pack({"side": "bottom"})
    lbl_nickname = Label(login_screen_frame, text="Your Nickname")
    lbl_nickname.pack()
    tb_nick = Text(login_screen_frame, width=50, height=5)
    tb_nick.pack()

# connect to server screen
def connect_server_screen():
    def get_address_port(tb_addr, tb_port):
    	addr = tb_addr.get("1.0", 'end-1c')
    	port = tb_port.get("1.0", 'end-1c')
	global nickname
    	player = new_player(nickname, addr, port)
    	if "error" in player:
	    error_message(player["error"])
    	else:
	    global proxy
	    proxy = player["proxy"]
	    global client_id
            client_id = player["client_id"]["client_id"]
            session_list = get_session_list(proxy)
            if "error" in session_list:
                error_message(session_list["error"])
            else:
                multiplayer_game_screen(session_list) 
    login_screen_frame.destroy()
    global connect_server_screen_frame
    connect_server_screen_frame = Tk()
    connect_server_screen_frame.title("Enter Sudoku server address")
    okay = Button(connect_server_screen_frame, text="ok", command=lambda:get_address_port(tb_addr, tb_port), width=20)
    okay.pack({"side": "bottom"})
    lbl_address = Label(connect_server_screen_frame, text="Server Address",font=("Arial", 10))
    lbl_address.pack()
    tb_addr = Text(connect_server_screen_frame, width=50, height=2, font=("Arial", 10))
    tb_addr.pack()
    lbl_port = Label(connect_server_screen_frame, text="Server Port",font=("Arial", 10))
    lbl_port.pack()
    tb_port = Text(connect_server_screen_frame, width=50, height=2,font=("Arial", 10))
    tb_port.pack()

# multiplayer game screen
def multiplayer_game_screen(list_sessions):

    def on_select(event):
	widget = event.widget
	global session_id
	global proxy
    	session_id = int(widget.get(widget.curselection()))
        status = join_session(proxy, client_id, session_id)
        if "error" in status:
            error_message(status["error"])
        else:
            start_game_screen(status)

    connect_server_screen_frame.destroy()
    global multiplayer_game_screen_frame
    multiplayer_game_screen_frame = Tk()
    multiplayer_game_screen_frame.title("Multiplayer Game Dialog ")
    lb_sessions = Listbox(multiplayer_game_screen_frame,height = 5,font=("Arial", 10),selectmode='single')
    lb_sessions.bind('<<ListboxSelect>>', on_select)
    for session in list_sessions:
        lb_sessions.insert(END, session["session_id"])
    lb_sessions.pack()
    btn_okay = Button(multiplayer_game_screen_frame, text="New Session", command = new_session_screen, width=20)
    btn_okay.pack({"side": "bottom"})

# new session screen
def new_session_screen():

    def session(tb_player_number):
    	player_number = tb_player_number.get("1.0", 'end-1c')
    	if player_number is not None:
	    global client_id
	    print client_id
	    global session_id
	    global proxy
            session = new_session(proxy, client_id, player_number)
	    
            if "error" in session:
            	error_message(session["error"])
            else:
                status = join_session(proxy, client_id, session["session_id"])
                start_game_screen(status)

    multiplayer_game_screen_frame.destroy()
    global new_session_screen_frame
    new_session_screen_frame = Tk()
    new_session_screen_frame.title("New Sudoku Solving Session")
    lbl_player_number = Label(new_session_screen_frame, text="Number of Players:")
    lbl_player_number.pack()
    tb_player_number = Text(new_session_screen_frame, width=50, height=2)
    tb_player_number.pack()
    btn_okay = Button(new_session_screen_frame, text="Ok", command = lambda: session(tb_player_number), width=20)
    btn_okay.pack({"side": "bottom"})

# start game screen
def start_game_screen(status):
    if not new_session_screen_frame:
    	new_session_screen_frame.destroy()
    if not multiplayer_game_screen_frame:
    	multiplayer_game_screen_frame.destroy()

    global sudoku_app
    sudoku_screen_frame = Tk()
    # TODO : Wait till all users connected! (Desired player count reached!)
    sudoku_app = SudokuApp(sudoku_screen_frame, status["game"])

# wait screen
def waiting_screen():
    global sudoku_app
    sudoku_screen_frame = Tk()
    # TODO : Wait till all users connected! (Desired player count reached!)
    sudoku_app = SudokuApp(sudoku_screen_frame, status["game"])


if __name__ == '__main__':
    a_path = sep.join(abspath(argv[0]).split(sep)[:-1])
    # Append script working directory into PYTHONPATH
    path.append(a_path)
    login_screen()
    mainloop()
