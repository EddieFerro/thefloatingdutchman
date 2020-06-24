from pygame import Vector2

from character.player.player_data import PlayerData
from character.player.player_sprite import PlayerSprite
from game_settings import WINDOW_HEIGHT, WINDOW_WIDTH
from manager import Manager


class PlayerManager(Manager):
    def __init__(self):
        self._player = None

    def spawn(self):
        player_data = PlayerData(100, 1000, Vector2(
            WINDOW_WIDTH/2, WINDOW_HEIGHT/2), 10)
        self._player = PlayerSprite(player_data)

    def draw(self, screen):
        screen.blit(self._player.image, self._player.rect)
        self._player._bullets.draw(screen)

    def update(self, screen):
        self._player.update(screen)

    @property
    def player(self):
        return self._player
