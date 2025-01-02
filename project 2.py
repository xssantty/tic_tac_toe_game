import pygame
import sys

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 600, 700  # Увеличили высоту экрана для размещения текста
LINE_WIDTH = 15
BOARD_ROWS, BOARD_COLS = 3, 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4

# Цвета
LIGHT_THEME = {
    'bg': (255, 255, 255),
    'line': (0, 0, 0),
    'circle': (0, 0, 255),
    'cross': (255, 0, 0),
    'text': (0, 0, 0)
}

DARK_THEME = {
    'bg': (0, 0, 0),
    'line': (255, 255, 255),
    'circle': (0, 255, 255),
    'cross': (255, 0, 255),
    'text': (255, 255, 255)
}

# Текущая тема
current_theme = LIGHT_THEME

# Шрифты
pygame.font.init()
font = pygame.font.SysFont('comicsans', 40)
small_font = pygame.font.SysFont('comicsans', 30)

# Инициализация экрана
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Крестики-нолики")

# Игровые переменные
board = [[None for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
player = "X"
game_over = False
winner = None
player_names = {"X": "", "O": ""}
scores = {"X": 0, "O": 0}

# Функция для рисования сетки
def draw_grid():
    # Горизонтальные линии
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(screen, current_theme['line'], (0, 100 + i * SQUARE_SIZE), (WIDTH, 100 + i * SQUARE_SIZE), LINE_WIDTH)
    # Вертикальные линии
    for i in range(1, BOARD_COLS):
        pygame.draw.line(screen, current_theme['line'], (i * SQUARE_SIZE, 100), (i * SQUARE_SIZE, 100 + 3 * SQUARE_SIZE), LINE_WIDTH)

# Функция для рисования крестиков и ноликов
def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == "X":
                # Рисуем крестик
                start_x = col * SQUARE_SIZE + SPACE
                start_y = row * SQUARE_SIZE + SPACE + 100
                end_x = (col + 1) * SQUARE_SIZE - SPACE
                end_y = (row + 1) * SQUARE_SIZE - SPACE + 100
                pygame.draw.line(screen, current_theme['cross'], (start_x, start_y), (end_x, end_y), CROSS_WIDTH)
                pygame.draw.line(screen, current_theme['cross'], (end_x, start_y), (start_x, end_y), CROSS_WIDTH)
            elif board[row][col] == "O":
                # Рисуем нолик
                center_x = col * SQUARE_SIZE + SQUARE_SIZE // 2
                center_y = row * SQUARE_SIZE + SQUARE_SIZE // 2 + 100
                pygame.draw.circle(screen, current_theme['circle'], (center_x, center_y), CIRCLE_RADIUS, LINE_WIDTH)

# Функция для проверки победителя
def check_winner():
    global winner, game_over

    # Проверка по строкам
    for row in range(BOARD_ROWS):
        if board[row][0] == board[row][1] == board[row][2] and board[row][0] is not None:
            winner = board[row][0]
            game_over = True
            return True

    # Проверка по столбцам
    for col in range(BOARD_COLS):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] is not None:
            winner = board[0][col]
            game_over = True
            return True

    # Проверка по диагоналям
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        winner = board[0][0]
        game_over = True
        return True
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        winner = board[0][2]
        game_over = True
        return True

    # Проверка на ничью
    if all(board[row][col] is not None for row in range(BOARD_ROWS) for col in range(BOARD_COLS)):
        winner = None
        game_over = True
        return True

    return False

# Функция для сброса доски
def reset_board():
    global board, player, game_over, winner
    board = [[None for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
    player = "X"
    game_over = False
    winner = None

# Функция для отображения текста
def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

# Функция для ввода имен игроков
def get_player_names():
    global player_names
    input_active = True
    input_text = ""
    current_player = "X"

    while input_active:
        screen.fill(current_theme['bg'])
        draw_text(f"Введите имя игрока {current_player}:", font, current_theme['text'], WIDTH // 2, HEIGHT // 2 - 50)
        draw_text(input_text, font, current_theme['text'], WIDTH // 2, HEIGHT // 2)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    player_names[current_player] = input_text
                    input_text = ""
                    if current_player == "X":
                        current_player = "O"
                    else:
                        input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

# Основной игровой цикл
def main():
    global player, game_over, winner, current_theme

    get_player_names()

    while True:
        screen.fill(current_theme['bg'])

        # Отображение счета
        draw_text(f"{player_names['X']}: {scores['X']}", small_font, current_theme['text'], WIDTH // 4, 30)
        draw_text(f"{player_names['O']}: {scores['O']}", small_font, current_theme['text'], 3 * WIDTH // 4, 30)

        # Отображение текущего игрока
        draw_text(f"Ход: {player_names[player]}", small_font, current_theme['text'], WIDTH // 2, HEIGHT - 30)

        # Если игра не завершена, рисуем сетку и фигуры
        if not game_over:
            draw_grid()
            draw_figures()

        # Проверка на победу
        if game_over:
            # Скрываем сетку и фигуры, отображаем сообщение о победе
            if winner:
                draw_text(f"Победил {player_names[winner]}!", font, current_theme['text'], WIDTH // 2, HEIGHT // 2)
                scores[winner] += 1
            else:
                draw_text("Ничья!", font, current_theme['text'], WIDTH // 2, HEIGHT // 2)
            pygame.display.update()
            pygame.time.wait(3000)
            reset_board()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                mouseX, mouseY = event.pos
                clicked_row = (mouseY - 100) // SQUARE_SIZE
                clicked_col = mouseX // SQUARE_SIZE

                if 0 <= clicked_row < BOARD_ROWS and 0 <= clicked_col < BOARD_COLS:
                    if board[clicked_row][clicked_col] is None:
                        board[clicked_row][clicked_col] = player
                        if check_winner():
                            game_over = True
                        else:
                            player = "O" if player == "X" else "X"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_t:
                    current_theme = DARK_THEME if current_theme == LIGHT_THEME else LIGHT_THEME

        pygame.display.update()

if __name__ == "__main__":
    main()