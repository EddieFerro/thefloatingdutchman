from pygame import Surface

from thefloatingdutchman.manager import Manager


class Room(Manager):
    def __init__(self):
        super().__init__()
        self._level = 0
        self._id = 0

    def spawn(self, level: int, _id: int):
        self._level = level
        self._id = _id

    def update(self):
        pass

    def draw(self, screen: Surface):
        pass

    @property
    def id(self):
        return self._id
