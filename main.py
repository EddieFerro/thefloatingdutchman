import os

import pygame

from thefloatingdutchman.game_manager import GameManager
# from game_manager import GameManager

os.environ['SDL_AUDIODRIVER'] = 'dsp'  # this removes audio error warnings


def main():
    pygame.init()

    game_manager = GameManager()
    game_manager.run()

    pygame.quit()


if __name__ == '__main__':
    main()
