class Board:
    def __init__(self, rows=15, cols=15):
        self.rows = rows
        self.cols = cols
        self.board = [['-' for _ in range(cols)] for _ in range(rows)]
        self.size = rows * cols

    def display(self):
        for row in self.board:
            print(' '.join(row))
        print('-' * (self.cols * 2 - 1))
    def undo_piece(self, row, col):
        self.board[row][col] = '-'
        self.size += 1
    def place_piece(self, row, col, symbol):
        """Place `symbol` at (row, col). Return True if valid move, False otherwise."""
        if 0 <= row < self.rows and 0 <= col < self.cols and self.board[row][col] == '-':
            self.board[row][col] = symbol
            self.size -= 1
            return True
        return False

    def check_win(self, symbol):
        """Return True if `symbol` has five in a row."""
        # horizontal
        for r in range(self.rows):
            for c in range(self.cols - 4):
                if all(self.board[r][c+i] == symbol for i in range(5)):
                    return True
        # vertical
        for c in range(self.cols):
            for r in range(self.rows - 4):
                if all(self.board[r+i][c] == symbol for i in range(5)):
                    return True
        # diag down-right
        for r in range(self.rows - 4):
            for c in range(self.cols - 4):
                if all(self.board[r+i][c+i] == symbol for i in range(5)):
                    return True
        # diag up-right
        for r in range(4, self.rows):
            for c in range(self.cols - 4):
                if all(self.board[r-i][c+i] == symbol for i in range(5)):
                    return True
        return False

    def is_full(self):
        """Return True if the board is full."""
        return self.size == 0
