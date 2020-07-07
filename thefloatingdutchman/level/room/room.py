from pygame import Surface

from thefloatingdutchman.character.enemy.enemy_manager import EnemyManager
from thefloatingdutchman.character.player.player_sprite import PlayerSprite
from thefloatingdutchman.manager import Manager


class Room(Manager):
    def __init__(self):
        self._enemy_manager = EnemyManager()
        self._level = 0
        self._id = 0

    def spawn(self, level: int, _id: int):
        self._level = level
        self._id = _id
        self._cleared = False
        self._enemy_manager.spawn(level)

    def update(self, player: PlayerSprite, screen: Surface):
        if self._enemy_manager.get_enemy_count():
            self._enemy_manager.update(player, screen)

    def get_enemies(self):
        return self._enemy_manager._enemies

    def cleared(self) -> bool:
        return not self._enemy_manager.get_enemy_count()

    def draw(self, screen: Surface):
        self._enemy_manager.draw(screen)

    @property
    def id(self):
        return self._id
