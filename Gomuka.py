import pygame
import random

# Initialize Pygame
pygame.init()

# Set up display
SCREEN_SIZE = 600
GRID_SIZE = 15
SQUARE_SIZE = SCREEN_SIZE // GRID_SIZE
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("Gomoku")

# Colors
BACKGROUND_COLOR = (240, 220, 180)
LINE_COLOR = (0, 0, 0)
BLACK_PIECE_COLOR = (0, 0, 0)
WHITE_PIECE_COLOR = (255, 255, 255)
BUTTON_COLOR = (200, 200, 200)

# Font
font = pygame.font.Font(None, 36)

# Game state
board = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]  # None = empty, '⚫' = black, '⚪' = white
current_player = '⚫'  # '⚫' for black (player), '⚪' for white (AI)
game_mode = None
game_over = False

def evaluate_window(window, ai_symbol, opp_symbol):
    ai_count = window.count(ai_symbol)
    opp_count = window.count(opp_symbol)
    empty_count = window.count(None)

    if ai_count == 5:
        return 100000
    if opp_count == 5:
        return -100000
    if ai_count == 4 and empty_count == 1:
        return 10000
    if opp_count == 4 and empty_count == 1:
        return -10000
    if ai_count == 3 and empty_count == 2:
        return 1000
    if opp_count == 3 and empty_count == 2:
        return -1000
    if ai_count == 3 and empty_count == 1:
        return 500
    if opp_count == 3 and empty_count == 1:
        return -500
    if ai_count == 2 and empty_count == 3:
        return 100
    if opp_count == 2 and empty_count == 3:
        return -100

 

    return ai_count - opp_count


def evaluate_board(board_obj, ai_symbol):
    opp = '⚫' if ai_symbol == '⚪' else '⚪'
    score = 0
    R, C = len(board_obj), len(board_obj[0])

    for r in range(R):
        for c in range(C - 4):
            score += evaluate_window(board_obj[r][c:c+5], ai_symbol, opp)

    for c in range(C):
        for r in range(R - 4):
            score += evaluate_window([board_obj[r+i][c] for i in range(5)], ai_symbol, opp)

    for r in range(R - 4):
        for c in range(C - 4):
            score += evaluate_window([board_obj[r+i][c+i] for i in range(5)], ai_symbol, opp)

    for r in range(4, R):
        for c in range(C - 4):
            score += evaluate_window([board_obj[r-i][c+i] for i in range(5)], ai_symbol, opp)

    return score

def get_candidate_moves(board):
    neighbors = set()
    R, C = len(board), len(board[0])
    found_piece = False

    for r in range(R):
        for c in range(C):
            if board[r][c] is not None:
                found_piece = True
                for dr in range(-1, 2):
                    for dc in range(-1, 2):
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < R and 0 <= nc < C and board[nr][nc] is None:
                            neighbors.add((nr, nc))
    
    if not found_piece:
        return [(R // 2, C // 2)]  # Start from the center if no pieces are on the board.

    return list(neighbors)

def minimax(board, depth, maximizing, ai_symbol):
    if depth == 0:
        return evaluate_board(board, ai_symbol), None

    opp_symbol = '⚫' if ai_symbol == '⚪' else '⚪'
    valid_moves = get_candidate_moves(board)
    best_move = None

    if maximizing:
        max_eval = float('-inf')
        for row, col in valid_moves:
            board[row][col] = ai_symbol
            ev, _ = minimax(board, depth - 1, False, ai_symbol)
            board[row][col] = None
            if ev > max_eval:
                max_eval, best_move = ev, (row, col)
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for row, col in valid_moves:
            board[row][col] = opp_symbol
            ev, _ = minimax(board, depth - 1, True, ai_symbol)
            board[row][col] = None
            if ev < min_eval:
                min_eval, best_move = ev, (row, col)
        return min_eval, best_move
    
# Alpha-beta 
def alpha_prun(board, depth, maximizing, ai_symbol, alpha, beta):
    if depth == 0:
        return evaluate_board(board, ai_symbol), None

    opp_symbol = '⚫' if ai_symbol == '⚪' else '⚪'
    valid_moves = get_candidate_moves(board)
    best_move = None

    if maximizing:
        max_eval = float('-inf')
        for row, col in valid_moves:
            board[row][col] = ai_symbol
            ev, _ = alpha_prun(board, depth - 1, False, ai_symbol, alpha, beta)
            board[row][col] = None
            if ev > max_eval:
                max_eval, best_move = ev, (row, col)
            alpha = max(alpha, ev)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for row, col in valid_moves:
            board[row][col] = opp_symbol
            ev, _ = alpha_prun(board, depth - 1, True, ai_symbol, alpha, beta)
            board[row][col] = None
            if ev < min_eval:
                min_eval, best_move = ev, (row, col)
            beta = min(beta, ev)
            if beta <= alpha:
                break
        return min_eval, best_move






def draw_board():
    screen.fill(BACKGROUND_COLOR)
    for row in range(GRID_SIZE):
        pygame.draw.line(screen, LINE_COLOR, (0, row * SQUARE_SIZE), (SCREEN_SIZE, row * SQUARE_SIZE), 2)
        pygame.draw.line(screen, LINE_COLOR, (row * SQUARE_SIZE, 0), (row * SQUARE_SIZE, SCREEN_SIZE), 2)

    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            piece = board[row][col]
            if piece == '⚫':
                pygame.draw.circle(screen, BLACK_PIECE_COLOR, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 2 - 5)
            elif piece == '⚪':
                pygame.draw.circle(screen, WHITE_PIECE_COLOR, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 2 - 5)

    pygame.display.flip()

def handle_click(pos):
    global current_player, game_over
    row, col = pos[1] // SQUARE_SIZE, pos[0] // SQUARE_SIZE

    if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE and board[row][col] is None and not game_over:
        board[row][col] = current_player
        if check_win(row, col, current_player):
            print(f"{current_player} wins!")
            game_over = True
        current_player = '⚪' if current_player == '⚫' else '⚫'

def check_win(row, col, player):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]
    for dr, dc in directions:
        count = 1
        r, c = row + dr, col + dc
        while 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE and board[r][c] == player:
            count += 1
            r += dr
            c += dc
        r, c = row - dr, col - dc
        while 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE and board[r][c] == player:
            count += 1
            r -= dr
            c -= dc
        if count >= 5:
            return True
    return False

def draw_menu():
    screen.fill(BACKGROUND_COLOR)
    title = font.render("Gomoku Game", True, LINE_COLOR)
    screen.blit(title, (SCREEN_SIZE // 2 - title.get_width() // 2, 100))
    draw_button("Player vs AI", 150, 200)
    draw_button("AI vs AI", 150, 300)
    pygame.display.flip()

def draw_button(text, x, y):
    button_rect = pygame.Rect(x, y, 300, 50)
    pygame.draw.rect(screen, BUTTON_COLOR, button_rect)
    text_surface = font.render(text, True, (0, 0, 0))
    screen.blit(text_surface, (x + (300 - text_surface.get_width()) // 2, y + (50 - text_surface.get_height()) // 2))
    return button_rect

def handle_menu_click(pos):
    global game_mode
    if pygame.Rect(150, 200, 300, 50).collidepoint(pos):
        game_mode = 0
    elif pygame.Rect(150, 300, 300, 50).collidepoint(pos):
        game_mode = 1

# Game loop
running = True
in_game = False
ai_delay = 500  # delay between AI moves (in ms)
last_ai_move_time = pygame.time.get_ticks()

while running:
    # Handle quit and mouse clicks
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not in_game:
                handle_menu_click(pygame.mouse.get_pos())
                if game_mode is not None:
                    in_game = True
                    game_over = False  # reset
                    current_player = '⚫'
            elif game_mode == 0 and not game_over:
                if current_player == '⚫':
                    handle_click(pygame.mouse.get_pos())

    # Player vs AI mode
    if in_game and game_mode == 0 and not game_over:
        if current_player == '⚪':
            _, best_move = minimax(board, 2, True, '⚪')
            if best_move:
                r, c = best_move
                board[r][c] = '⚪'
                if check_win(r, c, '⚪'):
                    print("AI wins!")
                    game_over = True
                current_player = '⚫'

 

    if in_game and game_mode == 1 and not game_over:
        current_time = pygame.time.get_ticks()
        if current_time - last_ai_move_time >= ai_delay:
            if current_player == '⚪':
                _, best_move = minimax(board, 2, True, '⚪')
                if best_move:
                    r, c = best_move
                    board[r][c] = '⚪'
                    if check_win(r, c, '⚪'):
                        print("Minimax wins!")
                        game_over = True
                current_player = '⚫'

            elif current_player == '⚫':
                _, best_move = alpha_prun(board, 3, True, '⚫', float('-inf'), float('inf'))
                if best_move:
                    r, c = best_move
                    board[r][c] = '⚫'
                    if check_win(r, c, '⚫'):
                        print("Alpha-beta wins!")
                        game_over = True
                current_player = '⚪'

            last_ai_move_time = current_time



    # Draw the board or menu
    if not in_game:
        draw_menu()
    else:
        draw_board()

    pygame.display.flip()

    # End game after a short delay
    if game_over:
        pygame.time.wait(2000)
        running = False
