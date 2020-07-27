from pygame import Surface

from thefloatingdutchman.manager import Manager
from thefloatingdutchman.utility.resource_container import ResourceContainer


class Room(Manager):
    def __init__(self, res_container: ResourceContainer):
        super().__init__(res_container)
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
