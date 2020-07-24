from pygame import display, time

from thefloatingdutchman.game_settings import WINDOW_WIDTH, WINDOW_HEIGHT, FPS
import thefloatingdutchman.ui as ui


class MenuManager:
    def __init__(self):
        self._screen = display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
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
