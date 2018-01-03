def list_diff(lst1, lst2):
    """Return lst1 - lst2.

    list_diff(list<X>, list<X>) -> list<X>
    The result is the list of entries in lst1 that are not in lst2.

    """
    diff = []
    for e in lst1:
        if not e in lst2:
            diff.append(e)
    return diff

def list_intersection(lst1, lst2):
    """Return the intersection.

    list_intersection(list<X>, list<X>) -> list<X>
    The result is the list of all entries in both lst1 and lst2.

    """
    inter = []
    for e in lst1:
        if e in lst2:
            inter.append(e)
    return inter

class Sudoku:
    """A Sudoku game"""

    # all the valid choices
    all_choices = ['1', '2', '3', '4', '5', '6', '7', '8', '9']

    def __init__(self, game=None):
     
        self.sudoku_board = [["4","3","5","2","6","9","7","8","1"],
               ["6","8","2","5","7","1","4","9","3"],
               ["1","9","7","8","3","4","5","6","2"],
               ["8","2","6","1","9","5","3","4","7"],
               ["3","7","4","6","8","2","9","1","5"],
               ["9","5","1","7","4","3","6","2","8"],
               ["5","1","9","3","2","6","8","7","4"],
               ["2","4","8","9","5","7","1","3","6"],
               ["7","6","3","4","1","8","2","5","9"]]

        self._game = [[" "," "," ","2","6"," ","7"," ","1"],
               ["6","8"," "," ","7"," "," ","9"," "],
               ["1","9"," "," "," ","4","5"," "," "],
               ["8","2"," ","1"," "," "," ","4"," "],
               [" "," ","4","6"," ","2","9"," "," "],
               [" ","5"," "," "," ","3"," ","2","8"],
               [" "," ","9","3"," "," "," ","7","4"],
               [" ","4"," "," ","5"," "," ","3","6"],
               ["7"," ","3"," ","1","8"," "," "," "]]
	if game:
	    self.sudoku_board = game[0]
	    self._game = game[1]

    def get_row(self, r):
      
        return self._game[r]

    def get_column(self, c):
       
        column = []
        for r in self._game:
            column.append(r[c])   
        return column

    def get_block(self, r, c):
       
        block = []
        for row in range(3*int(r), 3*int(r)+3):
            block.extend(self._game[row][3*int(c):3*int(c)+3])
        return block

    def get_entry(self, r, c):
        return self._game[r][c]

    def set_entry(self, r, c, v):
        self._game[r][c] = v

    def __getitem__(self, key):
        r,c = key
        return self._game[r][c]

    def __setitem__(self, key, val):
        r,c = key
        self.set_entry(r,c,val)
   
    def choices(self, r, c):
        block_row = r / 3
        block_col = c / 3
        row_choices = list_diff(Sudoku.all_choices, self.get_row(r))
        col_choices = list_diff(Sudoku.all_choices, self.get_column(c))
        block_choices = list_diff(Sudoku.all_choices, 
                                  self.get_block(block_row, block_col))
        choices = list_intersection(row_choices, col_choices)
        choices = list_intersection(choices, block_choices)
        return choices

    def check (self, i, j, value):
	# TODO : oosudoku mantigi daha basarili oyun mantigina calisacak vaktimiz olursa onu yapalim
        if self.sudoku_board[i][j] == value:
            self._game[i][j] = value
            if self.sudoku_board == self._game:
                return 1, True
            return 1, False
        else:
            return -1, False

    def get_puzzle (self):
        return self._game

    def get_board (self):
        return self.sudoku_board
