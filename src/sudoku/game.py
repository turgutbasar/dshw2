class Sudoku(object):
    def __init__(self):
        self.sudoku_board = [["4","3","5","2","6","9","7","8","1"],
               ["6","8","2","5","7","1","4","9","3"],
               ["1","9","7","8","3","4","5","6","2"],
               ["8","2","6","1","9","5","3","4","7"],
               ["3","7","4","6","8","2","9","1","5"],
               ["9","5","1","7","4","3","6","2","8"],
               ["5","1","9","3","2","6","8","7","4"],
               ["2","4","8","9","5","7","1","3","6"],
               ["7","6","3","4","1","8","2","5","9"]]
        self.sudoku_puzzle = [[" "," "," ","2","6"," ","7"," ","1"],
               ["6","8"," "," ","7"," "," ","9"," "],
               ["1","9"," "," "," ","4","5"," "," "],
               ["8","2"," ","1"," "," "," ","4"," "],
               [" "," ","4","6"," ","2","9"," "," "],
               [" ","5"," "," "," ","3"," ","2","8"],
               [" "," ","9","3"," "," "," ","7","4"],
               [" ","4"," "," ","5"," "," ","3","6"],
               ["7"," ","3"," ","1","8"," "," "," "]]

    def check (self, i, j, value):
        if self.sudoku_board[i][j] == value:
            self.sudoku_puzzle[i][j] = value
            if self.sudoku_board == self.sudoku_puzzle:
                return 1, True
            return 1, False
        else:
            return -1, False
    def get_puzzle (self):
        return self.sudoku_puzzle
    def get_board (self):
        return self.sudoku_board
