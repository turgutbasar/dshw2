# Imports----------------------------------------------------------------------
# Main method -----------------------------------------------------------------

from Tkinter import *
import tkMessageBox
from gui.game_screen import SudokuApp
from rpc.client import get_session_list, new_player, new_session, join_session
from os.path import abspath, sep
from sys import path,argv

def get_nickname():
    global nickname
    nickname = nick_text.get("1.0",'end-1c')
    if (nickname != '') and (' ' not in nickname) and len(nickname) <= 8:
        write_names = open("nicknames", "a")
        write_names.write("\n"+nickname)
        connect_to_server()
    else:
        error_message("your nickname is not valid")


def error_message(message):
    tkMessageBox.showerror("Title", message)

def info_message(message):
    tkMessageBox.showinfo("Title", message)

def on_select(event):
    #print event.widget.curselection()[0]
    global nickname
    nickname = list_name.get(list_name.curselection())
    connect_to_server()

# show nickname screen
def create_login_screen():
    read_names = open("nicknames", "r")
    names = read_names.read().split()
    global login
    login = Tk()
    login.title("Enter Nickname")
    global list_name
    list_name = Listbox(login, selectmode='single')
    list_name.bind('<<ListboxSelect>>', on_select)
    i = 0
    for n in names:
        list_name.insert(i,n)
        i+=1
    list_name.pack()
    okay = Button(login, text="ok", command=get_nickname, width=20)
    okay.pack({"side": "bottom"})
    nick_label = Label(login, text="Your Nickname")
    nick_label.pack()
    global nick_text
    nick_text = Text(login, width=50, height=5)
    nick_text.pack()
    mainloop()
# connect to server screen
def connect_to_server():
    login.destroy()
    global root
    root = Tk()
    root.title("Enter Sudoku server address")
    okay = Button(root, text="ok", command=get_address_port, width=20)
    okay.pack({"side": "bottom"})
    address_label = Label(root, text="server address",font=("Arial", 10))
    address_label.pack()
    global address_text
    address_text = Text(root, width=50, height=2, font=("Arial", 10))
    address_text.pack()
    port_label = Label(root, text="port",font=("Arial", 10))
    port_label.pack()
    global port_text
    port_text = Text(root, width=50, height=2,font=("Arial", 10))
    port_text.pack()
    mainloop()

def get_address_port():
    address_server = address_text.get("1.0", 'end-1c')
    port = port_text.get("1.0", 'end-1c')
    global proxy
    global client_id
    player = new_player(nickname, address_server, port)
    if "error" in player:
        error_message(player["error"])
    else:
        proxy = player["proxy"]
        client_id = player["client_id"]
        if player is not None:
            list_sessions = get_session_list(player["proxy"])
            if "error" in list_sessions:
                error_message(list_sessions["error"])
            else:
                multiplayer_game(list_sessions)


def create_game_screen(status):
    print status
    if status["isAvailable"]:
        if "game" in status:
            game = status["game"]
            print game
#            sudoku = Tk()
#            app = SudokuApp(sudoku)
#            mainloop()
        else:
            print "game is not ready"
    else:
        print "click event"

    mainloop()

def on_click_sessions(event):
    global session_id
    global status
    session_id = int(list_box_sessions.get(list_box_sessions.curselection()))
    if proxy is not None and client_id is not None and session_id is not None:
        status = join_session(proxy, client_id["client_id"], session_id)
        if "error" in status:
            error_message(status["error"])
        else:
            create_game_screen(status)


def multiplayer_game(list_sessions):
    root.destroy()
    global game
    game = Tk()
    game.title("Multiplayer Game Dialog ")
    global list_box_sessions
    list_box_sessions = Listbox(game,height = 5,font=("Arial", 10),selectmode='single')
    list_box_sessions.bind('<<ListboxSelect>>', on_click_sessions)
    i = 0
    for n in list_sessions:
        list_box_sessions.insert(i, n["session_id"])
        i += 1
    list_box_sessions.pack()
    okay = Button(game, text="create new session", command = create_session, width=20)
    okay.pack({"side": "bottom"})
    mainloop()

def create_session():
    print("create sesson")
    game.destroy()
    global session
    session = Tk()
    session.title("Creating new Sudoku Solving Session")
    okay = Button(session, text="ok", command = create_new_session, width=20)
    okay.pack({"side": "bottom"})
    num_label = Label(session, text="Player's number:")
    num_label.pack()
    global player_number
    player_number = Text(session, width=50, height=2)
    player_number.pack()
    mainloop()

def create_new_session():
    global session_id
    desired_number = player_number.get("1.0", 'end-1c')
    if desired_number is not None:
        session_id = new_session(proxy, client_id["client_id"], desired_number)
        print session_id
        if "error" in session_id:
            error_message(session_id["error"])
        else:
            if session_id is not None:
                 status = join_session(proxy, client_id["client_id"], session_id["session_id"])
                 print client_id
                 create_game_screen(status)

def game_player_scenario():
    print "senario"

if __name__ == '__main__':
    a_path = sep.join(abspath(argv[0]).split(sep)[:-1])
    # Append script working directory into PYTHONPATH
    path.append(a_path)
    create_login_screen()





