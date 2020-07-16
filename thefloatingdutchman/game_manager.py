import os
from pygame import display, event, time, QUIT, KEYDOWN, K_TAB

from thefloatingdutchman.character.player.player_manager import PlayerManager
from thefloatingdutchman.manager import Manager
from thefloatingdutchman.game_settings import WINDOW_WIDTH, WINDOW_HEIGHT, FPS
from thefloatingdutchman.level.room.room_manager import RoomManager
import thefloatingdutchman.ui as ui


class GameManager(Manager):
    def __init__(self):
        super().__init__()
        self._screen = display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self._game_over_screen = ui.GameOverScreen()  # game over screen
        self._pause_screen = ui.PauseScreen()
        self._done = False
        self._level = 0
        path = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), "space_images/space4.jpg")
        self._background = ui.image_fill_background(path)
        self._tutorial = ui.TutorialElements()
        # can go ahead and construct managers
        # since their spawn function controls their state
        self._player_manager = PlayerManager()
        self._room_manager = RoomManager()

    def run(self):
        self.spawn()
        # comment out this line to remove the tutorial
        self._tutorial.spawn_tutorial(self._screen)

        while not self._done:
            time.Clock().tick(FPS)  # setting fps not sure if it works tho
            for e in event.get():
                if e.type == QUIT:  # user closes application
                    self._done = True  # game over

                elif e.type == KEYDOWN and e.key == K_TAB:
                    # will eventually be moved
                    self._done, restart_game, view_map, view_game_controls = self._pause_screen.pause_screen_options(
                        self._pause_screen.draw_screens(self._screen, 0))
                    if restart_game:
                        self.spawn()
                    elif view_map:
                        self._done = self._room_manager.render_map(
                            self._screen)
                    elif view_game_controls:
                        self._tutorial.spawn_game_controls(self._screen)

            self.update()
            self.draw()

    # resets game
    def spawn(self):
        self._level = 0
        self._level_surface = ui.LevelSurface()
        self._player_manager.spawn()
        self._room_manager.spawn(self._level)

    def update(self):
        self._room_manager.update(self._player_manager.player, self._screen)
        self._player_manager.update(
            self._screen, self._room_manager.get_current_enemies())
        ui.health_bar(self._screen, self._player_manager)

        if self._room_manager.is_level_cleared():
            self._level += 1
            self._level_surface.draw_new_level(self._level)
            self._room_manager.spawn(self._level)

        if self._player_manager.player.dead:
            self._done = self._game_over_screen.game_over_screen_options(
                self._game_over_screen.draw_screens(self._screen, 0))
            if not self._done:
                self.spawn()

        if self._room_manager.is_room_cleared():  # enemies gone

            # must check if player died to last enemy exploding
            if self._player_manager.player.dead:
                self._done = self._game_over_screen.game_over_screen_options(
                    self._game_over_screen.draw_screens(self._screen, 0))
                if not self._done:
                    self.spawn()
            else:
                self._done = self._room_manager.render_map(self._screen)

                self._player_manager.player._data.pos.update(
                    WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
            time.wait(200)

    def draw(self):
        self._screen.blit(self._background, self._background.get_rect())
        self._screen.blit(self._background, self._background.get_rect())
        self._player_manager.draw(self._screen)
        ui.health_bar(self._screen, self._player_manager)
        self._level_surface.update_screen_level(self._screen)
        self._room_manager.draw(self._screen)
        display.flip()
