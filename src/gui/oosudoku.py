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

    def _read_game(self, game):
        for row in game:
            self._game.append(row)


    def __init__(self, game_arr):
     
        self._game = []
        self._read_game(game_arr)

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
