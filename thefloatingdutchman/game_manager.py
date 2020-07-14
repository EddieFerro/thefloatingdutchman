import os
from pygame import display, event, time, K_m, QUIT, KEYDOWN, K_TAB, Surface, transform

from thefloatingdutchman.character.player.player_manager import PlayerManager
from thefloatingdutchman.manager import Manager
from thefloatingdutchman.game_settings import WINDOW_WIDTH, WINDOW_HEIGHT, FPS
from thefloatingdutchman.level.room.room_manager import RoomManager
from thefloatingdutchman.user_interface.map_ui import MapUI
import thefloatingdutchman.ui as ui


class GameManager(Manager):
    def __init__(self):
        super().__init__()
        self._idealScreen = Surface((1920, 1080))
        self._user_info = display.Info()
        self._screen = display.set_mode((self._user_info.current_w, self._user_info.current_h))
        self._game_over_screen = ui.GameOverScreen()  # game over screen
        self._pause_screen = ui.PauseScreen()
        self._map = MapUI()
        self._done = False
        self._level = 0
        path = os.path.join(os.path.dirname(os.path.realpath(__file__)),"space_images/space4.jpg")
        self._background = ui.image_fill_background(path)
        self._tutorial = ui.TutorialElements()
        # can go ahead and construct managers
        # since their spawn function controls their state
        self._player_manager = PlayerManager()
        self._room_manager = RoomManager()

    def run(self):
        self.spawn()
        # comment out this line to remove the tutorial
        self._tutorial.spawn_tutorial(self._idealScreen, self._screen)

        while not self._done:
            time.Clock().tick(FPS)  # setting fps not sure if it works tho
            for e in event.get():
                if e.type == QUIT:  # user closes application
                    # will eventually be moved
                    self._done = True  # game over

                elif e.type == KEYDOWN and e.key == K_TAB:
                    # will eventually be moved
                    self._done, restart_game, view_map, view_game_controls = self._pause_screen.pause_screen_options(self._pause_screen.draw_screens(self._idealScreen,0))
                    if restart_game:
                        self.spawn()
                    elif view_map:
                        self._done = self._map.render(
                            self._idealScreen,
                            self._room_manager.rooms,
                            self._room_manager.get_available_rooms(),
                            self._room_manager.current_room_id,
                            self._room_manager.set_current_room,
                            self._screen
                        )
                    elif view_game_controls:
                        self._tutorial.spawn_game_controls(self._idealScreen, self._screen)

            self.update()
            self.draw()

            if self._player_manager.player.dead:  # enemies gone
                self._done = self._game_over_screen.game_over_screen_options(self._game_over_screen.draw_screens(self._idealScreen,0))
                if self._done is False:
                    self.spawn()
            if self._room_manager._rooms[self._room_manager._current_room_id].cleared():
                self.update()
                if self._player_manager.player.dead:  # enemies gone
                    self._done = self._game_over_screen.game_over_screen_options(self._game_over_screen.draw_screens(self._idealScreen,0))
                    if self._done is False:
                        self.spawn()
                else:
                    self._done = self._map.render(
                        self._idealScreen,
                        self._room_manager.rooms,
                        self._room_manager.get_available_rooms(),
                        self._room_manager.current_room_id,
                        self._room_manager.set_current_room,
                        self._screen
                    )
                    self._player_manager.player._data.pos.update(WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
                time.wait(200)

    # resets game

    def spawn(self):
        self._level = 0
        self._level_surface = ui.LevelSurface()
        self._player_manager.spawn()
        self._room_manager.spawn(self._level)
        self._map.spawn(self._room_manager)

    def update(self):
        self._player_manager.update(
            self._idealScreen, self._room_manager.get_current_enemies())
        self._room_manager.update(self._player_manager.player, self._idealScreen)

        if self._room_manager.is_level_cleared():
            self._level += 1
            self._level_surface.draw_new_level(self._level)
            self._room_manager.spawn(self._level)
            self._map.spawn(self._room_manager)


    def draw(self):
        self._idealScreen.blit(self._background, self._background.get_rect())
        self._idealScreen.blit(self._background, self._background.get_rect())
        self._player_manager.draw(self._idealScreen)
        ui.health_bar(self._idealScreen, self._player_manager)
        self._level_surface.update_screen_level(self._idealScreen)
        self._room_manager.draw(self._idealScreen)
        temp_trans = transform.scale(self._idealScreen, (display.Info().current_w, display.Info().current_h))
        self._screen.blit(temp_trans, temp_trans.get_rect())
        display.flip()