from pygame import Surface

from thefloatingdutchman.manager import Manager
<<<<<<< HEAD
from ...objects.drop_manager import DropManager
=======
>>>>>>> origin/master


class Room(Manager):
    def __init__(self):
<<<<<<< HEAD
        self._enemy_manager = EnemyManager()
        self._drop_manager = DropManager()
=======
        super().__init__()
>>>>>>> origin/master
        self._level = 0
        self._id = 0

    def spawn(self, level: int, _id: int):
        self._level = level
        self._id = _id
<<<<<<< HEAD
        self._cleared = False
        self._enemy_manager.spawn(level)
        self._drop_manager.spawn(level)


    def update(self, player: PlayerSprite, screen: Surface):
        self._drop_manager.update(player, screen, player)
        if self._enemy_manager.get_enemy_count():
            self._enemy_manager.update(player, screen)

    def get_enemies(self):
        return self._enemy_manager._enemies

    def cleared(self) -> bool:
        return not self._enemy_manager.get_enemy_count()

    def draw(self, screen: Surface):
        self._enemy_manager.draw(screen)



=======

    def update(self):
        pass

    def draw(self, screen: Surface):
        pass
>>>>>>> origin/master

    @property
    def id(self):
        return self._id
