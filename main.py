import character

import pygame

import os

os.environ['SDL_AUDIODRIVER'] = 'dsp' # this removes audio error warnings
WIDTH = 1000
HEIGHT = 800


def spawn(is_enemy, health, fire_rate, spawn_position_x, spawn_position_y, velx, vely, passed_list):
    if is_enemy is False:
        player1 = character.Player(health, fire_rate, spawn_position_x, spawn_position_y, velx, vely)
        passed_list.add(player1.player_sprite)
    else:
        enemy1 = character.Enemy(health, fire_rate, spawn_position_x, spawn_position_y, velx, vely)
        passed_list.add(enemy1.enemy_sprite)

def newScreenHelper(screen, width, height, fontSize, text, textColor, resizeWidth, resizeHeight, fill): # inserts surface onto screen
    surface = pygame.Surface((width, height), pygame.SRCALPHA) # create surface
    if fill: # fill surface with color
        surface.fill(fill)
    font = pygame.font.SysFont('Comic Sans MS', fontSize) # font
    text = font.render(text, True, textColor) # create text
    surface.blit(text,((surface.get_rect().width - text.get_width()) / 2, (surface.get_rect().height - text.get_height()) / 2)) # center text onto surface
    screen.blit(surface, ((WIDTH-surface.get_width())/resizeWidth, (HEIGHT-surface.get_height())/resizeHeight)) # position surface onto screen
    return screen

def gameOverScreen(screen):
    screen.fill('black')

    screen = newScreenHelper(screen, WIDTH/2, HEIGHT/5, 100, "GAME OVER!", (255,255,255), 2, 4, None) # game over
    screen = newScreenHelper(screen, WIDTH/4, HEIGHT/10, 50, "PLAY AGAIN", (255,255,255), 2, 2, (0,255,0)) # play again
    screen = newScreenHelper(screen, WIDTH/4, HEIGHT/10, 50, "QUIT", (255,255,255), 2, 3/2, (0,0,0)) # quit

    pygame.display.update() #update screen
    return screen

def pauseScreen(screen):
    pygame.draw.rect(screen, (255,255,255), (WIDTH/5, HEIGHT/5, WIDTH/(5/3), HEIGHT/(5/3)))
    screen = newScreenHelper(screen, WIDTH/2, HEIGHT/5, 100, "PAUSE", (0,0,0), 2, 4, None) # game over
    screen = newScreenHelper(screen, WIDTH/4, HEIGHT/10, 50, "RESUME", (255,255,255), 2, 2, (0,255,0)) # play again
    screen = newScreenHelper(screen, WIDTH/4, HEIGHT/10, 50, "QUIT", (255,255,255), 2, 3/2, (0,0,0)) # quit

    pygame.display.update()
    return screen

def screenOptions(screen, gameOver):
    playAgain = True # indicates which option is highlighted
    mouseDown = False # mouse action only activated when hovering over correct surface
    while True:
        ev = 2 # indicates option to select when user users arrow key
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN or (event.type == pygame.MOUSEBUTTONDOWN and mouseDown):
                if event.type != pygame.MOUSEBUTTONDOWN and event.key == pygame.K_DOWN: # quit highlighted
                    ev = 1
                elif event.type != pygame.MOUSEBUTTONDOWN and event.key == pygame.K_UP: # play again highlighted
                    ev = 0
                if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1) or event.key == pygame.K_RETURN: # button selected
                    if playAgain:
                        return False
                    else:
                        return True

        mouseDown = False
        mouse = pygame.mouse.get_pos()
        if ((WIDTH*(5/8)) >= mouse[0] >= (WIDTH*(3/8)) or ev < 2): # user hovers over proper width
            if gameOver: text = "PLAY AGAIN"
            else: text = "RESUME"
            if ((HEIGHT*(11/20)) >= mouse[1] >= (HEIGHT*(9/20)) or ev == 0): # user hovers over Play Again button
                screen = newScreenHelper(screen, WIDTH/4, HEIGHT/10, 50, text, (255,255,255), 2, 2, (0,255,0)) # play again
                screen = newScreenHelper(screen, WIDTH/4, HEIGHT/10, 50, "QUIT", (255,255,255), 2, 3/2, (0,0,0)) # quit
                playAgain = True
                mouseDown = True
            elif ((HEIGHT*(7/10)) >= mouse[1] >= (HEIGHT*(3/5)) or ev == 1): # user hovers over quit button
                screen = newScreenHelper(screen, WIDTH/4, HEIGHT/10, 50, "QUIT", (255,255,255), 2, 3/2, 'red') # quit
                screen = newScreenHelper(screen, WIDTH/4, HEIGHT/10, 50, text, (255,255,255), 2, 2, (0,0,0)) # play again
                playAgain = False
                mouseDown = True
        pygame.display.update() # update screen

def main():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    players = pygame.sprite.Group()
    enemies = pygame.sprite.Group()

    # Used for basic spawning testing
    spawn(False, 100, 2, WIDTH / 2, HEIGHT / 2, 10, 10, players)
    spawn(True, 100, 2, 50, 50, 8, 8, enemies)
    spawn(True, 100, 2, 500, 500, 8, 8, enemies)

    done = False
    while not done:
        pygame.time.Clock().tick(60)  # setting fps not sure if it works tho
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # user closes application
                screen = gameOverScreen(screen) # game over screen
                done = screenOptions(screen, True) # will eventually be moved
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
                screen = pauseScreen(screen)
                done = screenOptions(screen, False)

        # Used for basic spawning testing

        players.update()
        enemies.update()
        screen.fill((0, 0, 0))
        players.draw(screen)
        enemies.draw(screen)
        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()
