import pygame
#import os

#os.environ['SDL_AUDIODRIVER'] = 'dsp' #this removes audio error warnings

def main():
    pygame.init()

    screen = pygame.display.set_mode((400, 300))
    done = False

    while not done:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        done = True

if __name__ == '__main__': 
    main()