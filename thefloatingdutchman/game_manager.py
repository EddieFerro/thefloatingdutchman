import os
import sys
from pygame import display, event, time, K_m, QUIT, KEYDOWN, K_TAB

from thefloatingdutchman.character.player.player_manager import PlayerManager
from thefloatingdutchman.manager import Manager
from thefloatingdutchman.game_settings import WINDOW_WIDTH, WINDOW_HEIGHT, FPS
from thefloatingdutchman.level.room.room_manager import RoomManager
import thefloatingdutchman.ui as ui


class GameManager(Manager):
    def __init__(self):
        super().__init__()
        self._screen = display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self._main_menu = ui.MainMenu()
        self._game_over_screen = ui.GameOverScreen()  # game over screen
        self._pause_screen = ui.PauseScreen()
        self._done = False
        self._level = 0
        path = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), "space_images/space4.jpg")
        self._background = ui.image_fill_background(path)
        self._tutorial = ui.Tutorial()
        # can go ahead and construct managers
        # since their spawn function controls their state
        self._player_manager = PlayerManager()
        self._room_manager = RoomManager()

    def run(self):
        self._access_main_menu()
        self.spawn()
        # comment out this line to remove the tutorial
        #self._tutorial.begin_tutorial(self._screen)

        while not self._done:
            time.Clock().tick(FPS)  # setting fps not sure if it works tho
            for e in event.get():
                if e.type == QUIT:  # user closes application
                    self._done = True  # game over

                elif e.type == KEYDOWN and e.key == K_TAB:
                    # will eventually be moved
                    self._access_pause_screen()
            self.update()
            self.draw()

    # resets game
    def spawn(self):
        self._level = 1
        self._level_surface = ui.LevelSurface()
        self._player_manager.spawn()
        self._room_manager.spawn(self._level)

    def update(self):
        self._room_manager.update(self._player_manager.player, self._screen)
        self._player_manager.update(self._screen, self._room_manager.get_current_enemies())
        ui.health_bar(self._screen, self._player_manager)

        if self._room_manager.is_level_cleared():
            self._level += 1
            self._level_surface.draw_new_level(self._level)
            self._room_manager.spawn(self._level)

        if self._player_manager.player.dead:
            self._done = self._game_over_screen.open(
                self._game_over_screen.draw(self._screen, 0))
            if not self._done:
                self.spawn()

        if self._room_manager.is_room_cleared():  # enemies gone

            # must check if player died to last enemy exploding
            if self._player_manager.player.dead:
                self._done = self._game_over_screen.open(
                    self._game_over_screen.draw(self._screen, 0))
                if not self._done:
                    self.spawn()
            else:
                self._done = self._room_manager.render_map(self._screen)

                self._player_manager.player._data.pos.update(
                    WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
            time.wait(200)

    def draw(self):
        self._screen.blit(self._background, self._background.get_rect())
        self._player_manager.draw(self._screen)
        ui.health_bar(self._screen, self._player_manager)
        self._level_surface.update_screen(self._screen)
        self._room_manager.draw(self._screen)
        display.flip()

    def _access_main_menu(self):
        result = self._main_menu.open(self._main_menu.draw(self._screen, 0))
        if result == 2: #show game controls
            self._tutorial.show_game_controls(self._screen)
        if result == 3: #quit
            self._done = True

    def _access_pause_screen(self):
        result = self._pause_screen.open(self._pause_screen.draw(self._screen, 0))
        #outputs of 0 and 1 indicate to resume the game for now, resulting in no action
        if result == 2: #show map
            self._done = self._room_manager.render_map(self._screen)
        elif result == 3: #show game controls
            self._tutorial.show_game_controls(self._screen)
        elif result == 4: #restart game
            self.spawn()
        elif result == 5: #quit
            self._done = True
