import character

import pygame

import os

from game_settings import WINDOW_WIDTH, WINDOW_HEIGHT


os.environ['SDL_AUDIODRIVER'] = 'dsp'  # this removes audio error warnings


def spawn(is_enemy, health, fire_rate, spawn, vel, passed_list):

    if is_enemy is False:
        player1 = character.Player(
            health, fire_rate, spawn, vel)
        passed_list.add(player1.sprite)
    else:
        enemy1 = character.Enemy(
            health, fire_rate, spawn, vel)
        passed_list.add(enemy1.sprite)


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
    screen.fill('black')

    # game over text
    screen = newScreenHelper(screen, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 5, 100,
                             "GAME OVER!", (255, 255, 255), 2, 4, None)

    # play again button
    screen = newScreenHelper(screen, WINDOW_WIDTH / 4, WINDOW_HEIGHT / 10, 50, "PLAY AGAIN", (255, 255, 255), 2, 2,
                             (0, 255, 0))

    # quit button
    screen = newScreenHelper(screen, WINDOW_WIDTH / 4, WINDOW_HEIGHT / 10,
                             50, "QUIT", (255, 255, 255), 2, 3 / 2, (0, 0, 0))

    pygame.display.update()  # update screen
    return screen


def pauseScreen(screen):
    pygame.draw.rect(screen, (255, 255, 255), (WINDOW_WIDTH / 4, WINDOW_HEIGHT / 6, WINDOW_WIDTH / 2, WINDOW_HEIGHT / (3 / 2)),
                     border_radius=int(min(WINDOW_WIDTH / 2, WINDOW_HEIGHT / (3 / 2)) / 4))
    screen = newScreenHelper(screen, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 5,
                             100, "PAUSED", (0, 0, 0), 2, 4, None)  # game over
    screen = newScreenHelper(screen, WINDOW_WIDTH / 4, WINDOW_HEIGHT / 10, 50, "RESUME", (255, 255, 255), 2, 2,
                             (0, 255, 0))  # play again
    screen = newScreenHelper(screen, WINDOW_WIDTH / 4, WINDOW_HEIGHT / 10,
                             50, "QUIT", (255, 255, 255), 2, 3 / 2, (0, 0, 0))  # quit

    pygame.display.update()
    return screen


def screenOptions(screen, gameOver):
    playAgain = True  # indicates which option is highlighted
    mouseDown = False  # mouse action only activated when hovering over correct surface
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
                screen = newScreenHelper(screen, WINDOW_WIDTH / 4, WINDOW_HEIGHT / 10, 50, text, (255, 255, 255), 2, 2,
                                         (0, 255, 0))  # play again
                screen = newScreenHelper(screen, WINDOW_WIDTH / 4, WINDOW_HEIGHT / 10, 50, "QUIT", (255, 255, 255), 2, 3 / 2,
                                         (0, 0, 0))  # quit
                playAgain = True
                mouseDown = True
            # user hovers over quit button
            elif ((WINDOW_HEIGHT * (7 / 10)) >= mouse[1] >= (WINDOW_HEIGHT * (3 / 5)) or ev == 1):
                screen = newScreenHelper(screen, WINDOW_WIDTH / 4, WINDOW_HEIGHT / 10, 50, "QUIT", (255, 255, 255), 2, 3 / 2,
                                         'red')  # quit
                screen = newScreenHelper(screen, WINDOW_WIDTH / 4, WINDOW_HEIGHT / 10, 50, text, (255, 255, 255), 2, 2,

                                         (0, 0, 0))  # play again
                playAgain = False
                mouseDown = True
        pygame.display.update()  # update screen


def main():
    pygame.init()

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    players = pygame.sprite.Group()
    enemies = pygame.sprite.Group()

    # Used for basic spawning testing
    # spawn(False, 100, 2, pygame.Vector2(
    #     WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2), 10, players)
    spawn(True, 100, 2, pygame.Vector2(50, 50), 8, enemies)
    spawn(True, 100, 2, pygame.Vector2(500, 500), 8, enemies)

    player1 = character.Player(
        100, 2, pygame.Vector2(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2), 10)

    players.add(player1.sprite)

    done = False
    while not done:
        pygame.time.Clock().tick(60)  # setting fps not sure if it works tho
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # user closes application
                screen = gameOverScreen(screen)  # game over screen
                done = screenOptions(screen, True)  # will eventually be moved
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
                screen = pauseScreen(screen)
                done = screenOptions(screen, False)

        # Used for basic spawning testing

        player1.sprite.update(screen)

        enemies.update(*players, enemies)
        screen.fill((0, 0, 0))
        players.draw(screen)
        enemies.draw(screen)
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
