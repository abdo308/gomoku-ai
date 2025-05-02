import copy, random
from Board import Board
from Player import Player

def evaluate_window(window, ai_symbol, opp_symbol):
    ai_count = window.count(ai_symbol)
    opp_count = window.count(opp_symbol)
    if ai_count == 4 and window.count('-') == 1:
        return 100000
    if opp_count == 4 and window.count('-') == 1:
        return -100000
    if ai_count == 3 and window.count('-') == 2:
        return 1000
    if opp_count == 3 and window.count('-') == 2:
        return -1000
    if ai_count == 2 and window.count('-') == 3:
        return 100
    if opp_count == 2 and window.count('-') == 3:
        return -100
    return (2 ** ai_count) - (2 ** opp_count)

def evaluate_board(board_obj, ai_symbol):
    opp = 'O' if ai_symbol == 'X' else 'X'
    score = 0
    B, R, C = board_obj.board, board_obj.rows, board_obj.cols
    # horizontal
    for r in range(R):
        for c in range(C - 4):
            score += evaluate_window(B[r][c:c+5], ai_symbol, opp)
    # vertical
    for c in range(C):
        for r in range(R - 4):
            score += evaluate_window([B[r+i][c] for i in range(5)], ai_symbol, opp)
    # diag down-right
    for r in range(R - 4):
        for c in range(C - 4):
            score += evaluate_window([B[r+i][c+i] for i in range(5)], ai_symbol, opp)
    # diag up-right
    for r in range(4, R):
        for c in range(C - 4):
            score += evaluate_window([B[r-i][c+i] for i in range(5)], ai_symbol, opp)
    return score

def get_candidate_moves(board_obj, radius=1):
    neighbors = set()
    for r in range(board_obj.rows):
        for c in range(board_obj.cols):
            if board_obj.board[r][c] != '-':
                for dr in range(-radius, radius + 1):
                    for dc in range(-radius, radius + 1):
                        nr, nc = r + dr, c + dc
                        if (0 <= nr < board_obj.rows and
                            0 <= nc < board_obj.cols and
                            board_obj.board[nr][nc] == '-'):
                            neighbors.add((nr, nc))
    if not neighbors:
        return [(board_obj.rows // 2, board_obj.cols // 2)]  # center if board is empty
    return list(neighbors)

def minimax(board_obj, depth, maximizing, ai_symbol):
    opp = 'O' if ai_symbol == 'X' else 'X'
    if depth == 0 or board_obj.is_full():
        return evaluate_board(board_obj, ai_symbol), None
    valid_moves = get_candidate_moves(board_obj)
    if not valid_moves:
        return evaluate_board(board_obj, ai_symbol), None
    best_move = None
    if maximizing:
        max_eval = float('-inf')
        for row, col in valid_moves:
            board_obj.place_piece(row, col, ai_symbol)
            if board_obj.check_win(ai_symbol):
                board_obj.undo_piece(row, col)
                return 100000, (row, col)
            ev, _ = minimax(board_obj, depth-1, False, ai_symbol)
            board_obj.undo_piece(row, col)
            if ev > max_eval:
                max_eval, best_move = ev, (row, col)
        if best_move is None:
            best_move = random.choice(valid_moves)
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for row, col in valid_moves:
            board_obj.place_piece(row, col, opp)
            if board_obj.check_win(opp):
                board_obj.undo_piece(row, col)
                return -100000, (row, col)
            ev, _ = minimax(board_obj, depth-1, True, ai_symbol)
            board_obj.undo_piece(row, col)
            if ev < min_eval:
                min_eval, best_move = ev, (row, col)
        if best_move is None:
            best_move = random.choice(valid_moves)
        return min_eval, best_move

def alphaBeta(board_obj, depth, alpha, beta, maximizing, ai_symbol):
    opp = 'O' if ai_symbol == 'X' else 'X'
    if depth == 0 or board_obj.is_full():
        return evaluate_board(board_obj, ai_symbol), None
    valid_moves = get_candidate_moves(board_obj)
    if not valid_moves:
        return evaluate_board(board_obj, ai_symbol), None
    best_move = None
    if maximizing:
        max_eval = float('-inf')
        for row, col in valid_moves:
            board_obj.place_piece(row, col, ai_symbol)
            if board_obj.check_win(ai_symbol):
                board_obj.undo_piece(row, col)
                return 100000, (row, col)
            ev, _ = alphaBeta(board_obj, depth-1, alpha, beta, False, ai_symbol)
            board_obj.undo_piece(row, col)
            if ev > max_eval:
                max_eval, best_move = ev, (row, col)
            alpha = max(alpha, ev)
            if beta <= alpha:
                break
        if best_move is None:
            best_move = random.choice(valid_moves)
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for row, col in valid_moves:
            board_obj.place_piece(row, col, opp)
            if board_obj.check_win(opp):
                board_obj.undo_piece(row, col)
                return -100000, (row, col)
            ev, _ = alphaBeta(board_obj, depth-1, alpha, beta, True, ai_symbol)
            board_obj.undo_piece(row, col)
            if ev < min_eval:
                min_eval, best_move = ev, (row, col)
            beta = min(beta, ev)
            if beta <= alpha:
                break
        if best_move is None:
            best_move = random.choice(valid_moves)
        return min_eval, best_move


class Game:
    def __init__(self):
        self.board = Board()
        self.players = [
            Player("Player 1", 'X', is_ai=False),
            Player("AI", 'O', is_ai=True)
        ]
        self.cur = 0

    def switch(self):
        self.cur = 1 - self.cur

    def play(self, human_piece='X', choice=1):
        # assign symbols based on human choice
        human_piece = human_piece.upper()
        if choice == '1':
            if human_piece == 'O':
                self.players[0].symbol = 'O'
                self.players[1].symbol = 'X'

            while True:
                self.board.display()
                p = self.players[self.cur]

                if p.is_ai:
                    _, (row, col) = minimax(self.board, depth=1, maximizing=True, ai_symbol=p.symbol)
                    print(f"{p.name} ({p.symbol}) plays ({row}, {col})")
                    self.board.place_piece(row, col, p.symbol)
                else:
                    while True:
                        try:
                            row = int(input(f"{p.name} ({p.symbol}) choose row (0-{self.board.rows-1}): "))
                            col = int(input(f"{p.name} ({p.symbol}) choose col (0-{self.board.cols-1}): "))
                            if 0 <= row < self.board.rows and 0 <= col < self.board.cols and self.board.board[row][col] == '-':
                                break
                        except:
                            pass
                        print("Invalid, try again.")
                    self.board.place_piece(row, col, p.symbol)

                # Check if game ends (win or draw)
                if self.board.check_win(p.symbol):
                    self.board.display()
                    print(f"*** {p.name} ({p.symbol}) WINS! ***")
                    return
                if self.board.is_full():
                    self.board.display()
                    print("*** The game is a draw! ***")
                    return

                self.switch()
        else:  # AI vs AI
            self.players[0].is_ai = True
            algo = True
            while True:
                self.board.display()
                p = self.players[self.cur]
                if algo:
                    _, (row, col) = minimax(self.board, depth=2, maximizing=True, ai_symbol=p.symbol)
                    print(f"{p.name} ({p.symbol}) plays ({row}, {col})")
                    self.board.place_piece(row, col, p.symbol)
                else:
                    _, (row, col) = alphaBeta(self.board, depth=3, alpha=float('-inf'), beta=float('inf'), maximizing=True, ai_symbol=p.symbol)
                    print(f"{p.name} ({p.symbol}) plays ({row}, {col})")
                    self.board.place_piece(row, col, p.symbol)

                # Check if game ends (win or draw)
                if self.board.check_win(p.symbol):
                    self.board.display()
                    print(f"*** {p.name} ({p.symbol}) WINS! ***")
                    return
                if self.board.is_full():
                    self.board.display()
                    print("*** The game is a draw! ***")
                    return

                algo = not algo
                self.switch()
