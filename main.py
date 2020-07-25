import os

import pygame

from thefloatingdutchman.menu_manager import MenuManager
from thefloatingdutchman.game_manager import GameManager
# from game_manager import GameManager

os.environ['SDL_AUDIODRIVER'] = 'dsp'  # this removes audio error warnings


def main():
    pygame.init()
     
    menu_manager = MenuManager()
    game_manager = GameManager()

    while True:
        result = menu_manager.run() 
        if result > 1:
            break
        game_manager.run(result)

    pygame.quit()


if __name__ == '__main__':
    main()
