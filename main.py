import os

import pygame

from thefloatingdutchman.menu_manager import MenuManager
from thefloatingdutchman.game_manager import GameManager
from thefloatingdutchman.utility.resource_container import ResourceContainer
from thefloatingdutchman.game_settings import WINDOW_WIDTH, WINDOW_HEIGHT

os.environ['SDL_AUDIODRIVER'] = 'dsp'  # this removes audio error warnings


def main():
    pygame.init()

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    resources = ResourceContainer()
    menu_manager = MenuManager(screen)
    game_manager = GameManager(screen, resources)

    while True:
        result = menu_manager.run()
        if result > 1:
            break
        game_manager.run(result)

    pygame.quit()


if __name__ == '__main__':
    main()
