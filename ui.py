
import pygame

from game_settings import (WINDOW_WIDTH, WINDOW_HEIGHT, BLACK, WHITE, RED, GREEN, WIDTH_LEFT_BOUND, WIDTH_RIGHT_BOUND, CONTINUE_HEIGHT_LOWER_BOUND, CONTINUE_HEIGHT_UPPER_BOUND, 
QUIT_HEIGHT_LOWER_BOUND, QUIT_HEIGHT_UPPER_BOUND)

# create surface
def newScreenHelper(width, height, fontSize, text,
                    textColor, fill):
    
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

    return surface

# initialize surfaces that compose the game over screen
def initializeGameOverScreen():
    # game over text
    surfaces = []
    surfaces.append(newScreenHelper(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 5, 100, "GAME OVER!", WHITE, None))

    # play again button
    surfaces.append(newScreenHelper(WINDOW_WIDTH / 4, WINDOW_HEIGHT / 10, 50, "PLAY AGAIN", WHITE, GREEN))

    # quit button
    surfaces.append(newScreenHelper(WINDOW_WIDTH / 4, WINDOW_HEIGHT / 10, 50, "QUIT", WHITE, BLACK))
    
    return surfaces

# initialize surfaces that compose the pause screen
def initializePauseScreen():
    surfaces = []
    surfaces.append(newScreenHelper(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 5, 100, "PAUSED", BLACK, None))  # pause
    surfaces.append(newScreenHelper(WINDOW_WIDTH / 4, WINDOW_HEIGHT / 10, 50, "RESUME", WHITE, GREEN))  # play again
    surfaces.append(newScreenHelper(WINDOW_WIDTH / 4, WINDOW_HEIGHT / 10, 50, "QUIT", WHITE, BLACK))  # quit
    
    return surfaces

# draw pre-defined surfaces onto screen
def drawScreens(screen, surfaces, threeElems):
    resizeHeights = [4,2,3/2] 
    if not threeElems: #when only two surfaces are being attached
        resizeHeights.pop(0)
    for surface, height in zip(surfaces, resizeHeights): #attach surfaces onto screen
        screen.blit(surface, ((WINDOW_WIDTH - surface.get_width()) / 2,
                          (WINDOW_HEIGHT - surface.get_height()) / height))
    pygame.display.update()  # update screen
    return screen

# fill screen and return screen with surfaces drawn onto it
def drawGameOverScreen(screen, surfaces):
    screen.fill(BLACK)
    return drawScreens(screen, surfaces, True)

# fill screen and return screen with surfaces drawn onto it
def drawPauseScreen(screen, surfaces):
    pygame.draw.rect(screen, WHITE, (WINDOW_WIDTH / 4, WINDOW_HEIGHT / 6, WINDOW_WIDTH / 2, WINDOW_HEIGHT / (3 / 2)),
                     border_radius=int(min(WINDOW_WIDTH / 2, WINDOW_HEIGHT / (3 / 2)) / 4))
    return drawScreens(screen, surfaces, True)

# fill screen and return screen with surfaces drawn onto it
def updateScreenOptions(screen, text, color1, color2):
    surfaces = []
    surfaces.append(newScreenHelper(WINDOW_WIDTH / 4, WINDOW_HEIGHT / 10, 50, text, WHITE, color1))  # play again
    surfaces.append(newScreenHelper(WINDOW_WIDTH / 4, WINDOW_HEIGHT / 10, 50, "QUIT", WHITE, color2))  # quit
    return drawScreens(screen, surfaces, False)


def screenOptions(screen, text):
    mostRecentIsContinue = True # used to determine whether the user just changed options
    
    while True:
        for event in pygame.event.get():
            mouse = pygame.mouse.get_pos() # mouse position
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION: # event has occurred

                # player has chosen an option
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:  #(event.type == pygame.MOUSEBUTTONDOWN and event.button == 1) or 
                    if mostRecentIsContinue: # either end program or continue it
                        return False
                    else:
                        return True

                # button may be highlighted/selected, user hovers over proper width
                if (event.type == pygame.KEYDOWN and (event.key == pygame.K_DOWN or event.key == pygame.K_UP)) or (WIDTH_RIGHT_BOUND >= mouse[0] >= WIDTH_LEFT_BOUND):
                    
                    # user hovers over Play Again button
                    if CONTINUE_HEIGHT_UPPER_BOUND >= mouse[1] >= CONTINUE_HEIGHT_LOWER_BOUND or (event.type == pygame.KEYDOWN and event.key == pygame.K_UP):
                        if not mostRecentIsContinue: # user selects Play Again/Resume after selecting Quit
                            screen = updateScreenOptions(screen, text, GREEN, BLACK)
                        mostRecentIsContinue = True
                        if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1): # player clicked on Continue button
                            return False

                    # user hovers over quit button
                    elif QUIT_HEIGHT_UPPER_BOUND >= mouse[1] >= QUIT_HEIGHT_LOWER_BOUND or (event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN): # user hovers over Quit Button
                        if mostRecentIsContinue: # user selects Quit after selecting Play Again/Resume
                            screen = updateScreenOptions(screen, text, BLACK, RED)
                        mostRecentIsContinue = False
                        if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1): # player clicked on Quit button
                            return True