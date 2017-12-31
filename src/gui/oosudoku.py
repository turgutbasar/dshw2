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

def row2list(str):
    """Convert a row string into a list

    row2list(string) -> list<char>
    Precondition: str is a string representation of a row i.e. every
    second char is an entry of the row and there are 9 entries

    """
    row = []
    for i in range(0, 18, 2):
        row.append(str[i])
    return row


class Sudoku:
    """A Sudoku game"""

    # all the valid choices
    all_choices = ['1', '2', '3', '4', '5', '6', '7', '8', '9']



    def _read_game(self, game):
        for row in game:
            self._game.append(row)


    def __init__(self, game_arr, autofill = False):
     
        self._game = []
        self._read_game(game_arr)
        self._undo_stack = []  # keeps move info for later undos
        self._do_auto_fill = autofill  # determine if auto fill should be used


    def write_game(self, filename):
        f = open(filename, 'w')
        for row in self._game:
            f.write(' '.join(row) + '\n')
        f.close()

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
        entries = [(r,c)]
        if self._do_auto_fill:
            auto = self.auto_fill()
            entries.extend(auto)
        self._undo_stack.append(entries)

    def undo(self):
     
        if self._undo_stack != []:
            entries = self._undo_stack.pop()
            for r,c in entries:
                self._game[r][c] = ' '
        
   

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


    def game_status(self):

        status = "Finished"

        game = self._game
        for row in range(9):
            for col in range(9):
               if game[row][col] == ' ':
                   status = ""
                   ch = self.choices(row, col)
                   scores = 0
                   if not ch:
                       k=scores-1
                       print k
                       return "Unsolvable"

        return status

    def flip_af(self):
     

        self._do_auto_fill = not self._do_auto_fill
        return self._do_auto_fill


    def auto_fill(self):
       
        fill = []
        found = True
        game = self._game
        while found:
            found = False
            for row in range(9):
                for col in range(9):
                    if game[row][col] != ' ': continue
                    ch = self.choices(row, col)
                    if len(ch) == 1:
                        found = True
                        fill.append((row,col))
                        game[row][col] = ch[0]
        return fill



    def __repr__(self):
        result = ''
        for row in self._game:
            result = result + ''.join(row) + '\n'
        return result
