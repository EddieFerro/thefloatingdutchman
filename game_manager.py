import pygame
from pygame import display, event, time, QUIT, KEYDOWN, K_TAB

from character.player.player_manager import PlayerManager
from manager import Manager
from game_settings import WINDOW_WIDTH, WINDOW_HEIGHT, BLACK, FPS, WHITE
from level.room.room import Room
import ui


class GameManager(Manager):
    def __init__(self):
        self._screen = display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self._game_over_screen = ui.initialize_game_over_screen()  # game over screen
        self._pause_screen = ui.initialize_pause_screen()
        self._done = False
        self._level = 0

        # can go ahead and construct managers
        # since their spawn function controls their state
        self._player_manager = PlayerManager()
        self._room = Room()

    def run(self):
        self.spawn()
        
        while not self._done:
            time.Clock().tick(FPS)  # setting fps not sure if it works tho
            for e in event.get():
                if e.type == QUIT:  # user closes application
                    # will eventually be moved
                    self._done = True# game over
                elif e.type == KEYDOWN and e.key == K_TAB:
                    # will eventually be moved
                    self._done = ui.screen_options(ui.draw_pause_screen(self._screen, self._pause_screen), "RESUME") # pause

            self.update()
            self.draw()

            if len(self._room._enemy_manager._enemies) is 0:
                self._done = ui.screen_options(ui.draw_game_over_screen(self._screen, self._game_over_screen),"PLAY AGAIN")  # game over
                if self._done is False:
                    self.spawn()

    # resets game

    def spawn(self):
        self._level = 0
        self._player_manager.spawn()
        self._room.spawn(self._level)

    def update(self):
        self._player_manager.update(self._screen)
        self._room.update(self._player_manager.player)

    def draw(self):
        self._screen.fill(BLACK)
        self._player_manager.draw(self._screen)
        self._room.draw(self._screen)
        display.flip()
