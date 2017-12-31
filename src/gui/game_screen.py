import Tkinter
from Tkinter import *
from oosudoku import *

large_font = ("Courier New", "21", "bold")

class NumberButtons(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent, relief=SUNKEN, bg = "grey")
        self.buttons = []
        self.current = IntVar()
        for i in range(1,10):
            bi = Radiobutton(self, text = str(i), value = i, 
                             variable = self.current,
                             indicatoron=0,
                             font = large_font, fg = "red",
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
                itemsid.append(self.CanvasGame.create_text(4+(2*i-1)*self.CanvasSize/18, 4+(2*j-1)*self.CanvasSize/18, anchor = CENTER, tag='Text', text = " ", font = large_font, fill="red"))
            self.table.append(itemsid)

        self.labelVariable = StringVar()
        self.labelVariable.set("")
        self.label = Label(self, textvariable=self.labelVariable, font = large_font, bg="grey", fg="red")
        self.label.pack(pady = 10)

        self.CanvasGame.bind("<Button-1>", self.Write) # If the player left-click on the canvas => execute the method Write

    def Write(self, event):
        items = self.CanvasGame.find_enclosed(event.x - 35,event.y -35 , event.x +35,event.y +35) # We consider all items enclosed in a square 70x70 where the user clicked (the size of the square depends strongly on the canvas.size) 
        item = list_intersection(items, self.CanvasGame.find_withtag('Text')) # We just consider previous selected items which are empty "case"(i.e. item with a tag 'Text')
        if len(item) == 1:
            for i in range(0,9):
                for j in range(0,9):
                    if int(item[0]) == int(self.table[j][i]):
                        if str(self.numberbuttons.get_current()) in self.sudoku.choices(i,j): # We check what the user tries to insert is consistent with the available choices
                            self.sudoku.set_entry(i,j,str(self.numberbuttons.get_current()))  # We Update game[][]
                            self.Update() # We update the display
       
    def Update(self):
        # Update the Label
        self.labelVariable.set(self.sudoku.game_status())
        # Update the Fixed Numbers --> All items which are "Fixed" tagged are displayed in red
        for i in range(0,9):
            for j in range(0,9):
                if " " not in self.sudoku._game[i][j]:
                    self.CanvasGame.itemconfig(self.table[j][i], text=self.sudoku._game[i][j], font = large_font, tag='Fixed', fill="red")
        
    def SetNumberButtons(self, numberbuttons):
        self.numberbuttons = numberbuttons

    def SetSudoku(self, sudoku):
        self.sudoku = sudoku

class Controller(Frame):
    """ Create:
        2 Frames : one contains a view instance(canvas + lable), the other contains a numberbuttons instance and a commands instance
    """
    def __init__(self, parent):
        Frame.__init__(self, parent, bg = "grey")
        self.parent = parent
        self.F1 = Frame(parent, bd=5, bg = "grey", relief="sunken")
        self.F2 = Frame(parent, bg="grey")
        self.view = View(self.F1)
        self.numberbuttons = NumberButtons(self.F2)
        self.view.SetNumberButtons(self.numberbuttons)
        
        #Display
        self.F1.pack(fill = Y, side=LEFT)
        self.F2.pack(fill = Y, side=LEFT)
        self.view.pack(side = LEFT, padx = 30)
        self.numberbuttons.pack(side = LEFT, padx = 20)

    def LoadGame(self, game):
        
        self.sudoku = Sudoku(game, False)
        self.view.SetSudoku(self.sudoku)
        self.view.Update()

class SudokuApp():
    def __init__(self, master, game):
        master.title("Sudoku")
        master.config(bg = "grey")
        master.resizable(0,0)
        self.controller = Controller(master)
	self.controller.LoadGame(game.get_puzzle())
