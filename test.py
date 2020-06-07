import character

import pygame

# import os

# os.environ['SDL_AUDIODRIVER'] = 'dsp' #this removes audio error warnings
WIDTH = 1000
HEIGHT = 800




def spawn(is_enemy, health, fire_rate, spawn_position_x, spawn_position_y, velx, vely, passed_list):
    if is_enemy is False:
        player1 = character.Player(health, fire_rate, spawn_position_x, spawn_position_y, velx, vely)
        passed_list.add(player1.player_sprite)
    else:
        enemy1 = character.Enemy(health, fire_rate, spawn_position_x, spawn_position_y, velx, vely)
        passed_list.add(enemy1.enemy_sprite)


def main():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    players = pygame.sprite.Group()
    enemies = pygame.sprite.Group()

    # Used for basic spawning testing
    spawn(False, 100, 2, WIDTH / 2, HEIGHT / 2, 10, 10, players)
    spawn(True, 100, 2, 50, 50, 8, 8, enemies)
    spawn(True, 100, 2, 500, 500, 8, 8, enemies)


    running = True
    while running:
        pygame.time.Clock().tick(60)  # setting fps not sure if it works tho
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

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
