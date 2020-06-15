from pygame import display, event, time, QUIT, KEYDOWN, K_TAB

from character.player.player_manager import PlayerManager
from character.enemy.enemy_manager import EnemyManager
from manager import Manager
from game_settings import WINDOW_WIDTH, WINDOW_HEIGHT, BLACK, FPS
import ui


class GameManager(Manager):
    def __init__(self):
        self._screen = display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self._done = False

        # can go ahead and construct managers
        # since their spawn function controls their state
        self._player_manager = PlayerManager()
        self._enemy_manager = EnemyManager()

    def run(self):
        self.spawn()

        while not self._done:
            time.Clock().tick(FPS)  # setting fps not sure if it works tho
            for e in event.get():
                if e.type == QUIT:  # user closes application
                    self._screen = ui.gameOverScreen(
                        self._screen)  # game over screen

                    # will eventually be moved
                    self._done = ui.screenOptions(self._screen, True)
                elif e.type == KEYDOWN and e.key == K_TAB:
                    self._screen = ui.pauseScreen(self._screen)
                    self._done = ui.screenOptions(self._screen, False)

            self.update()
            self.draw()

    # resets game

    def spawn(self):
        self._player_manager.spawn()
        self._enemy_manager.spawn()

    def update(self):
        self._player_manager.update(self._screen)
        self._enemy_manager.update(self._player_manager.player)

    def draw(self):
        self._screen.fill(BLACK)
        self._player_manager.draw(self._screen)
        self._enemy_manager.draw(self._screen)
        display.flip()
