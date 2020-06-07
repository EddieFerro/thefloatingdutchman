import character
import pygame
#import os

#os.environ['SDL_AUDIODRIVER'] = 'dsp' #this removes audio error warnings
WIDTH = 1000
HEIGHT = 800

def main():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    done = False

    #Used for basic spawning testing

    # all_sprites = pygame.sprite.Group()
    # player = character.Player(100, 2, WIDTH/2, HEIGHT/2, 10,10)
    # enemy = character.Enemy(100, 2, 50, 50, 8, 8)
    # all_sprites.add(player.player_sprite)
    # all_sprites.add(enemy.enemy_sprite)

    while not done:
        pygame.time.Clock().tick(60) #setting fps not sure if it works tho
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
        
        #Used for basic spawning testing

        # all_sprites.update()
        # screen.fill((0,0,0))
        # all_sprites.draw(screen)
        # pygame.display.flip()
    

if __name__ == '__main__': 
    main()