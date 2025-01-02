import pygame

def get_player_names(screen, theme):
    player_names = {"X": "", "O": ""}
    input_active = True
    input_text = ""
    current_player = "X"

    while input_active:
        screen.fill(theme['bg'])
        font = pygame.font.SysFont('comicsans', 40)
        text_surface = font.render(f"Введите имя игрока {current_player}:", True, theme['text'])
        text_rect = text_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 50))
        screen.blit(text_surface, text_rect)

        input_surface = font.render(input_text, True, theme['text'])
        input_rect = input_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(input_surface, input_rect)

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

    return player_names
