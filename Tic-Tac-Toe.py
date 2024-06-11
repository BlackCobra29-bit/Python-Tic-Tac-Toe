import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
LINE_WIDTH = 15
BOARD_ROWS, BOARD_COLS = 3, 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4
# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BG_COLOR = (28, 170, 156)

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe")
screen.fill(BG_COLOR)

# Fonts
pygame.font.init()
font = pygame.font.SysFont("comicsans", 75)

# Board
board = [[" " for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

# Functions
def draw_lines():
    # Horizontal lines
    pygame.draw.line(screen, WHITE, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, WHITE, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)
    # Vertical lines
    pygame.draw.line(screen, WHITE, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)
    pygame.draw.line(screen, WHITE, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), LINE_WIDTH)


def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == "X":
                pygame.draw.line(screen, RED, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)
                pygame.draw.line(screen, RED, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                 CROSS_WIDTH)
            elif board[row][col] == "O":
                pygame.draw.circle(screen, BLUE, (int(col * SQUARE_SIZE + SQUARE_SIZE / 2),
                                                  int(row * SQUARE_SIZE + SQUARE_SIZE / 2)), CIRCLE_RADIUS,
                                   CIRCLE_WIDTH)


def mark_square(row, col, player):
    board[row][col] = player


def available_square(row, col):
    return board[row][col] == " "


def is_board_full():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == " ":
                return False
    return True


def check_win(player):
    # Check rows
    for row in range(BOARD_ROWS):
        if board[row][0] == board[row][1] == board[row][2] == player:
            draw_win_line((row, 0), (row, 2))
            return True
    # Check columns
    for col in range(BOARD_COLS):
        if board[0][col] == board[1][col] == board[2][col] == player:
            draw_win_line((0, col), (2, col))
            return True
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] == player:
        draw_win_line((0, 0), (2, 2))
        return True
    if board[0][2] == board[1][1] == board[2][0] == player:
        draw_win_line((0, 2), (2, 0))
        return True
    return False


def draw_win_line(start, end):
    start_x = start[1] * SQUARE_SIZE + SQUARE_SIZE // 2
    start_y = start[0] * SQUARE_SIZE + SQUARE_SIZE // 2
    end_x = end[1] * SQUARE_SIZE + SQUARE_SIZE // 2
    end_y = end[0] * SQUARE_SIZE + SQUARE_SIZE // 2
    pygame.draw.line(screen, GREEN, (start_x, start_y), (end_x, end_y), LINE_WIDTH)


def draw_winner_text(player):
    winner_text = font.render(f"{player} wins!", True, WHITE)
    screen.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT // 2 - winner_text.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(2000)


def minimax(board, depth, is_maximizing):
    if check_win("X"):
        return -1
    elif check_win("O"):
        return 1
    elif is_board_full():
        return 0

    if is_maximizing:
        best_score = -float("inf")
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] == " ":
                    board[row][col] = "O"
                    score = minimax(board, depth + 1, False)
                    board[row][col] = " "
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float("inf")
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] == " ":
                    board[row][col] = "X"
                    score = minimax(board, depth + 1, True)
                    board[row][col] = " "
                    best_score = min(score, best_score)
        return best_score


def get_best_move():
    best_score = -float("inf")
    best_move = ()
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == " ":
                board[row][col] = "O"
                score = minimax(board, 0, False)
                board[row][col] = " "
                if score > best_score:
                    best_score = score
                    best_move = (row, col)
    return best_move


def restart_game():
    screen.fill(BG_COLOR)
    draw_lines()
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            board[row][col] = " "


def main():
    player_turn = random.choice(["X", "O"])
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and player_turn == "X":
                x = event.pos[1] // SQUARE_SIZE
                y = event.pos[0] // SQUARE_SIZE
                if available_square(x, y):
                    mark_square(x, y, "X")
                    if check_win("X"):
                        draw_winner_text("X")
                        restart_game()
                    player_turn = "O"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    restart_game()

        if player_turn == "O" and not is_board_full():
            row, col = get_best_move()
            mark_square(row, col, "O")
            if check_win("O"):
                draw_winner_text("O")
                restart_game()
            player_turn = "X"

        screen.fill(BG_COLOR)
        draw_lines()
        draw_figures()
        if is_board_full() and not check_win("X") and not check_win("O"):
            draw_winner_text("Tie")
            restart_game()

        pygame.display.update()
        pygame.time.delay(100)


if __name__ == "__main__":
    main()
