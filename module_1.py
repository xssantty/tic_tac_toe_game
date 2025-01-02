import pygame
import sys
from .utils.theme_manager import ThemeManager
from .utils.input_manager import get_player_names
from .exceptions import GameOverException

class TicTacToe:
    def init(self):
        self.width, self.height = 600, 700
        self.line_width = 15
        self.board_rows, self.board_cols = 3, 3
        self.square_size = self.width // self.board_cols
        self.circle_radius = self.square_size // 3
        self.cross_width = 25
        self.space = self.square_size // 4

        self.theme_manager = ThemeManager()
        self.current_theme = self.theme_manager.get_theme()

        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Крестики-нолики")

        self.board = [[None for _ in range(self.board_cols)] for _ in range(self.board_rows)]
        self.player = "X"
        self.game_over = False
        self.winner = None
        self.player_names = {"X": "", "O": ""}
        self.scores = {"X": 0, "O": 0}

    def draw_grid(self):
        for i in range(1, self.board_rows):
            pygame.draw.line(self.screen, self.current_theme['line'], (0, 100 + i * self.square_size), (self.width, 100 + i * self.square_size), self.line_width)
        for i in range(1, self.board_cols):
            pygame.draw.line(self.screen, self.current_theme['line'], (i * self.square_size, 100), (i * self.square_size, 100 + 3 * self.square_size), self.line_width)

    def draw_figures(self):
        for row in range(self.board_rows):
            for col in range(self.board_cols):
                if self.board[row][col] == "X":
                    start_x = col * self.square_size + self.space
                    start_y = row * self.square_size + self.space + 100
                    end_x = (col + 1) * self.square_size - self.space
                    end_y = (row + 1) * self.square_size - self.space + 100
                    pygame.draw.line(self.screen, self.current_theme['cross'], (start_x, start_y), (end_x, end_y), self.cross_width)
                    pygame.draw.line(self.screen, self.current_theme['cross'], (end_x, start_y), (start_x, end_y), self.cross_width)
                elif self.board[row][col] == "O":
                    center_x = col * self.square_size + self.square_size // 2
                    center_y = row * self.square_size + self.square_size // 2 + 100
                    pygame.draw.circle(self.screen, self.current_theme['circle'], (center_x, center_y), self.circle_radius, self.line_width)

    def check_winner(self):
        for row in range(self.board_rows):
            if self.board[row][0] == self.board[row][1] == self.board[row][2] and self.board[row][0] is not None:
                self.winner = self.board[row][0]
                self.game_over = True
                return True

        for col in range(self.board_cols):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] and self.board[0][col] is not None:
                self.winner = self.board[0][col]
                self.game_over = True
                return True

        if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0] is not None:
            self.winner = self.board[0][0]
            self.game_over = True
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[0][2] is not None:
            self.winner = self.board[0][2]
            self.game_over = True
            return True
        if all(self.board[row][col] is not None for row in range(self.board_rows) for col in range(self.board_cols)):
            self.winner = None
            self.game_over = True
            return True

        return False

    def reset_board(self):
        self.board = [[None for _ in range(self.board_cols)] for _ in range(self.board_rows)]
        self.player = "X"
        self.game_over = False
        self.winner = None

    def draw_text(self, text, font, color, x, y):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)

    def main(self):
        self.player_names = get_player_names(self.screen, self.current_theme)

        while True:
            self.screen.fill(self.current_theme['bg'])

            self.draw_text(f"{self.player_names['X']}: {self.scores['X']}", pygame.font.SysFont('comicsans', 30), self.current_theme['text'], self.width // 4, 30)
            self.draw_text(f"{self.player_names['O']}: {self.scores['O']}", pygame.font.SysFont('comicsans', 30), self.current_theme['text'], 3 * self.width // 4, 30)
            self.draw_text(f"Ход: {self.player_names[self.player]}", pygame.font.SysFont('comicsans', 30), self.current_theme['text'], self.width // 2, self.height - 30)

            if not self.game_over:
                self.draw_grid()
                self.draw_figures()

            if self.game_over:
                if self.winner:
                    self.draw_text(f"Победил {self.player_names[self.winner]}!", pygame.font.SysFont('comicsans', 40), self.current_theme['text'], self.width // 2, self.height // 2)
                    self.scores[self.winner] += 1
                else:
                    self.draw_text("Ничья!", pygame.font.SysFont('comicsans', 40), self.current_theme['text'], self.width // 2, self.height // 2)
                pygame.display.update()
                pygame.time.wait(3000)
                self.reset_board()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
                    mouseX, mouseY = event.pos
                    clicked_row = (mouseY - 100) // self.square_size
                    clicked_col = mouseX // self.square_size

                    if 0 <= clicked_row < self.board_rows and 0 <= clicked_col < self.board_cols:
                        if self.board[clicked_row][clicked_col] is None:
                            self.board[clicked_row][clicked_col] = self.player
                            if self.check_winner():
                                self.game_over = True
                            else:
                                self.player = "O" if self.player == "X" else "X"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_t:
                        self.current_theme = self.theme_manager.toggle_theme()

            pygame.display.update()


if name == "main":
    game = TicTacToe()
    game.main()
  
