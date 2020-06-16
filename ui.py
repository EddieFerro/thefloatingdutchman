
import pygame

from game_settings import WINDOW_WIDTH, WINDOW_HEIGHT, BLACK, WHITE, RED, GREEN


def newScreenHelper(screen, width, height, fontSize, text,
                    textColor, resizeWidth, resizeHeight, fill):
    
    # inserts surface onto screen
    surface = pygame.Surface(
        (width, height), pygame.SRCALPHA)  # create surface
    if fill:  # fill surface with color
        surface.fill(fill)

    font = pygame.font.SysFont('Comic Sans MS', fontSize)  # font
    text = font.render(text, True, textColor)  # create text

    # center text onto surface
    surface.blit(text, ((surface.get_rect().width - text.get_width()) / 2,
                        (surface.get_rect().height - text.get_height()) / 2))

    # position surface onto screen
    screen.blit(surface, ((WINDOW_WIDTH - surface.get_width()) / resizeWidth,
                          (WINDOW_HEIGHT - surface.get_height()) / resizeHeight))

    return screen


def gameOverScreen(screen):
    screen.fill(BLACK)

    # game over text
    screen = newScreenHelper(screen, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 5, 100,
                             "GAME OVER!", WHITE, 2, 4, None)

    # play again button
    screen = newScreenHelper(screen, WINDOW_WIDTH / 4, WINDOW_HEIGHT / 10, 50, "PLAY AGAIN", WHITE, 2, 2,
                             GREEN)

    # quit button
    screen = newScreenHelper(screen, WINDOW_WIDTH / 4, WINDOW_HEIGHT / 10,
                             50, "QUIT", WHITE, 2, 3 / 2, BLACK)

    #pygame.display.update()  # update screen
    
    return screen


def pauseScreen(screen):
    pygame.draw.rect(screen, WHITE, (WINDOW_WIDTH / 4, WINDOW_HEIGHT / 6, WINDOW_WIDTH / 2, WINDOW_HEIGHT / (3 / 2)),
                     border_radius=int(min(WINDOW_WIDTH / 2, WINDOW_HEIGHT / (3 / 2)) / 4))
    screen = newScreenHelper(screen, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 5,
                             100, "PAUSED", BLACK, 2, 4, None)  # game over
    screen = newScreenHelper(screen, WINDOW_WIDTH / 4, WINDOW_HEIGHT / 10, 50, "RESUME", WHITE, 2, 2,
                             GREEN)  # play again
    screen = newScreenHelper(screen, WINDOW_WIDTH / 4, WINDOW_HEIGHT / 10,
                             50, "QUIT", WHITE, 2, 3 / 2, BLACK)  # quit

    #pygame.display.update()
    
    return screen


def screenOptions(screen, gameOver):
    playAgain = True  # indicates which option is highlighted
    mouseDown = False  # mouse action only activated when hovering over correct surface
    mostRecentIsContinue = True
    pygame.display.update()
    
    while True:
        ev = 2  # indicates option to select when user users arrow key
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN or (event.type == pygame.MOUSEBUTTONDOWN and mouseDown):
                if event.type != pygame.MOUSEBUTTONDOWN and event.key == pygame.K_DOWN:  # quit highlighted
                    ev = 1
                elif event.type != pygame.MOUSEBUTTONDOWN and event.key == pygame.K_UP:  # play again highlighted
                    ev = 0
                if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1) or event.key == pygame.K_RETURN:  # button selected

                    if playAgain:
                        return False
                    else:
                        return True

        mouseDown = False
        mouse = pygame.mouse.get_pos()
        # user hovers over proper width
        if (WINDOW_WIDTH * (5 / 8)) >= mouse[0] >= (WINDOW_WIDTH * (3 / 8)) or ev < 2:

            if gameOver:
                text = "PLAY AGAIN"
            else:
                text = "RESUME"
            if ((WINDOW_HEIGHT * (11 / 20)) >= mouse[1] >= (
                    WINDOW_HEIGHT * (9 / 20)) or ev == 0):  # user hovers over Play Again button
                if not mostRecentIsContinue:
                    screen = newScreenHelper(screen, WINDOW_WIDTH / 4, WINDOW_HEIGHT / 10, 50, text, WHITE, 2, 2,
                                            GREEN)  # play again
                    screen = newScreenHelper(screen, WINDOW_WIDTH / 4, WINDOW_HEIGHT / 10, 50, "QUIT", WHITE, 2, 3 / 2,
                                            BLACK)  # quit
                    pygame.display.update() # update screen
                playAgain = True
                mouseDown = True
                mostRecentIsContinue = True
            # user hovers over quit button
            elif ((WINDOW_HEIGHT * (7 / 10)) >= mouse[1] >= (WINDOW_HEIGHT * (3 / 5)) or ev == 1):
                if mostRecentIsContinue:
                    screen = newScreenHelper(screen, WINDOW_WIDTH / 4, WINDOW_HEIGHT / 10, 50, "QUIT", WHITE, 2, 3 / 2,
                                            RED)  # quit
                    screen = newScreenHelper(screen, WINDOW_WIDTH / 4, WINDOW_HEIGHT / 10, 50, text, WHITE, 2, 2,

                                            BLACK)  # play again
                    pygame.display.update() # update screen
                playAgain = False
                mouseDown = True
                mostRecentIsContinue = False
