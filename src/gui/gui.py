# Imports----------------------------------------------------------------------
from Tkinter import *
import tkMessageBox
from rpc.client import get_session_list, new_player, new_session, join_session
from sudoku.game import Sudoku, list_intersection

class GUI():

    def __init__(self):
	self.__current_frame = None

    def new_screen(self, title):
	if self.__current_frame:
	    self.__current_frame.destroy()
	self.__current_frame = Tk()
    	self.__current_frame.title("Enter Nickname")
	def shutdown_ttk_repeat():
    	    self.__current_frame.eval('::ttk::CancelRepeat')
            self.__current_frame.destroy()
        self.__current_frame.protocol("WM_DELETE_WINDOW", shutdown_ttk_repeat)

    # show nickname screen
    def login_screen(self):
    	def on_select(event):
    	    widget = event.widget    	
	    self.__nickname = widget.get(int(widget.curselection()[0]))
    	    self.connect_server_screen()

        def get_nickname(tb_nick):
    	    nickname = tb_nick.get("1.0",'end-1c')
    	    if (nickname != '') and (' ' not in nickname) and len(nickname) <= 8:
		self.__nickname = nickname
            	write_names = open("nicknames", "a")
            	write_names.write("\n"+self.__nickname)
            	self.connect_server_screen()
            else:
            	error_message("your nickname is not valid")

    	read_names = open("nicknames", "r")
    	names = read_names.read().split()
    	self.new_screen("Enter Nickname")
    	lb_names = Listbox(self.__current_frame, selectmode='single')
    	lb_names.bind('<<ListboxSelect>>', on_select)
    	for name in names:
            lb_names.insert(END, name)
    	lb_names.pack()
    	btn_okay = Button(self.__current_frame, text="ok", command=lambda : get_nickname(tb_nick), width=20)
    	btn_okay.pack({"side": "bottom"})
    	lbl_nickname = Label(self.__current_frame, text="Your Nickname")
    	lbl_nickname.pack()
    	tb_nick = Text(self.__current_frame, width=50, height=5)
    	tb_nick.pack()

    # connect to server screen
    def connect_server_screen(self):

    	def get_address_port(tb_addr, tb_port):
    	    addr = tb_addr.get("1.0", 'end-1c')
    	    port = tb_port.get("1.0", 'end-1c')
    	    player = new_player(self.__nickname, addr, port)
    	    if "error" in player:
	    	self.error_message(player["error"])
    	    else:
	    	self.__proxy = player["proxy"]
            	self.__client_id = player["client_id"]["client_id"]
            	session_list = get_session_list(self.__proxy)
            	if "error" in session_list:
                    self.error_message(session_list["error"])
            	else:
                    self.multiplayer_game_screen(session_list) 
    	self.new_screen("Enter Sudoku server address")
	btn_okay = Button(self.__current_frame, text="ok", command=lambda:get_address_port(tb_addr, tb_port), width=20)
	btn_okay.pack({"side": "bottom"})
	lbl_address = Label(self.__current_frame, text="Server Address",font=("Arial", 10))
	lbl_address.pack()
	tb_addr = Text(self.__current_frame, width=50, height=2, font=("Arial", 10))
	tb_addr.pack()
	lbl_port = Label(self.__current_frame, text="Server Port",font=("Arial", 10))
	lbl_port.pack()
	tb_port = Text(self.__current_frame, width=50, height=2,font=("Arial", 10))
	tb_port.pack()

    # multiplayer game screen
    def multiplayer_game_screen(self, list_sessions):

        def on_select(event):
	    widget = event.widget
	    self.__session_id = int(widget.get(widget.curselection()))
            status = join_session(self.__proxy, self.__client_id, self.__session_id)
            if "error" in status:
            	error_message(status["error"])
            else:
	        if status["isAvailable"] and status["isGameStarted"]:
	            self.__game = status["game"]
                    self.start_game_screen()
	        elif status["isAvailable"] and not status["isGameStarted"]:
		    self.__game = status["game"]
		    self.waiting_screen()
	        else:
		    self.info_message("Game is not available!")

	self.new_screen("Multiplayer Game Dialog")
	lb_sessions = Listbox(self.__current_frame,height = 5,font=("Arial", 10),selectmode='single')
	lb_sessions.bind('<<ListboxSelect>>', on_select)
	for session in list_sessions:
            lb_sessions.insert(END, session["session_id"])
	lb_sessions.pack()
	btn_okay = Button(self.__current_frame, text="New Session", command = self.new_session_screen, width=20)
	btn_okay.pack({"side": "bottom"})

    # new session screen
    def new_session_screen(self):

    	def session(tb_player_number):
    	    player_number = tb_player_number.get("1.0", 'end-1c')
    	    if player_number is not None:
            	session = new_session(self.__proxy, self.__client_id, player_number)
	    
            	if "error" in session:
            	    self.error_message(session["error"])
            	else:
                    status = join_session(self.__proxy, self.__client_id, session["session_id"])
		    self.__game = status["game"]
		    if not status["isGameStarted"]:
		    	self.waiting_screen()
		    else:
		    	self.start_game_screen()
    
        self.new_screen("New Sudoku Solving Session")
	lbl_player_number = Label(self.__current_frame, text="Number of Players:")
	lbl_player_number.pack()
	tb_player_number = Text(self.__current_frame, width=50, height=2)
	tb_player_number.pack()
	btn_okay = Button(self.__current_frame, text="Ok", command = lambda: session(tb_player_number), width=20)
	btn_okay.pack({"side": "bottom"})

    # wait screen
    def waiting_screen(self):
	self.new_screen("Waiting Players")
	lbl_waiting = Label(self.__current_frame, text="Waiting Players...")
	lbl_waiting.pack()

    # start game screen
    def start_game_screen(self):
	self.new_screen("Sudoku Game")

	class NumberButtons(Frame):

    	    def __init__(self, parent):
        	Frame.__init__(self, parent, relief=SUNKEN, bg = "grey")
        	self.buttons = []
        	self.current = IntVar()
        	for i in range(1,10):
            	    bi = Radiobutton(self, text = str(i), value = i, 
                             variable = self.current,
                             indicatoron=0,
                             font = ("Courier New", "21", "bold"), fg = "red",
                             selectcolor="yellow")
            	    bi.pack(ipadx = 4,pady = 6)
            	    self.buttons.append(bi)
        	self.current.set(1)

    	    def get_current(self):
        	return self.current.get()
	class View(Frame):
    	    def __init__(self, parent):
            	Frame.__init__(self, parent, bg = "grey")

        	self.sudoku = None
        	self.numberbuttons = None

        	# Initialize the Canvas
        	self.CanvasSize = 500 
        	self.CanvasGame = Canvas(self, width = self.CanvasSize-2, height = self.CanvasSize-2, bg = "white", relief = "solid", bd = 4)
        	self.CanvasGame.pack(padx = 20, pady = 20)
        	self.table = []

        	# Create Canvas Items (Ligns + 9x9 Texts)  + 1 Label
        	for i in range(1,10):
            	    if (i == 3) or (i == 6): width = 4
            	    else: width = 1
            	    self.CanvasGame.create_line(4+i*self.CanvasSize/9, 0, 4+i*self.CanvasSize/9, self.CanvasSize+10, width = width, state="disabled")
            	    self.CanvasGame.create_line(0, 4+i*self.CanvasSize/9, self.CanvasSize+10, 4+i*self.CanvasSize/9, width = width, state="disabled")
            	    itemsid = []
            	    for j in range(1,10):
                        itemsid.append(self.CanvasGame.create_text(4+(2*i-1)*self.CanvasSize/18, 4+(2*j-1)*self.CanvasSize/18, anchor = CENTER, tag='Text', text = " ", font = ("Courier New", "21", "bold"), fill="red"))
            	    self.table.append(itemsid)

        	    self.labelVariable = StringVar()
        	    self.labelVariable.set("")
        	    self.label = Label(self, textvariable=self.labelVariable, font = ("Courier New", "21", "bold"), bg="grey", fg="red")
        	    self.label.pack(pady = 10)

        	    self.CanvasGame.bind("<Button-1>", self.Write) # If the player left-click on the canvas => execute the method Write

    	    def Update(self):
        	# Update the Label
        	self.labelVariable.set("")
        	# Update the Fixed Numbers --> All items which are "Fixed" tagged are displayed in red
        	for i in range(0,9):
            	    for j in range(0,9):
                	if " " not in self.sudoku._game[i][j]:
                    	    self.CanvasGame.itemconfig(self.table[j][i], text=self.sudoku._game[i][j], font = ("Courier New", "21", "bold"), tag='Fixed', fill="red")

	    def Write(self, event):
        	items = self.CanvasGame.find_enclosed(event.x - 35,event.y -35 , event.x +35,event.y +35) # We consider all items enclosed in a square 70x70 where the user clicked (the size of the square depends strongly on the canvas.size) 
        	item = list_intersection(items, self.CanvasGame.find_withtag('Text')) # We just consider previous selected items which are empty "case"(i.e. item with a tag 'Text')
        	if len(item) == 1:
            	    for i in range(0,9):
                	for j in range(0,9):
                    	    if int(item[0]) == int(self.table[j][i]):
                        	if str(self.numberbuttons.get_current()) in self.sudoku.choices(i,j): # We check what the user tries to insert is consistent with the available choices
				    # TODO : Send server our result and check answer
                            	    self.sudoku.set_entry(i,j,str(self.numberbuttons.get_current()))  # We Update game[][]
                            	    self.Update() # We update the display
        
            def SetNumberButtons(self, numberbuttons):
                self.numberbuttons = numberbuttons

            def SetSudoku(self, sudoku):
                self.sudoku = sudoku

        self.__current_frame.config(bg = "grey")
        self.__current_frame.resizable(0,0)
	# TODO : Implement broadcaster callback to update label below sudoku board
        F1 = Frame(self.__current_frame, bd=5, bg = "grey", relief="sunken")
        F2 = Frame(self.__current_frame, bg="grey")
        view = View(F1)
        numberbuttons = NumberButtons(F2)
        view.SetNumberButtons(numberbuttons)
        F1.pack(fill = Y, side=LEFT)
        F2.pack(fill = Y, side=LEFT)
        view.pack(side = LEFT, padx = 30)
        numberbuttons.pack(side = LEFT, padx = 20)
	view.SetSudoku(Sudoku())
        view.Update()
	# TODO : Detect application closes and send disconnect to server or implement a heartbeat to clean forced closes

    def error_message(self, message):
        tkMessageBox.showerror("Error", message)

    def info_message(self, message):
        tkMessageBox.showinfo("Info", message)

    def gui_start(self):
    	self.login_screen()
    	mainloop()    
