from pygame import time, Surface

from thefloatingdutchman.game_settings import FPS
import thefloatingdutchman.ui as ui


class MenuManager:
    def __init__(self, screen: Surface):
        self._screen = screen
        self._main_menu = ui.MainMenu()
        self._tutorial = ui.Tutorial()

    def run(self):  # loads main menu
        result = 0  # starts with highlighting Begin Game Option
        while True:  # continues until player either begins game or quits
            time.Clock().tick(FPS)  # setting fps not sure if it works tho
            result = self._main_menu.open(self._main_menu.draw(self._screen, result, self._main_menu._y_locations, False, None), result)
            if result == 2: #show game controls
                self._tutorial.show_game_controls(self._screen)
            else:  # option chosen
                return result
