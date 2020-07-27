from pygame.math import Vector2 as vec
from thefloatingdutchman.objects.object_data import ObjectData


class BulletData(ObjectData):
    def __init__(self, direction: vec, life_time: int, spawn: vec, vel: int, type5=False):
        super().__init__(spawn, vel)
        self._life_time = life_time
        self._direction = direction
        self.type5 = type5

    @property
    def life_time(self) -> int:
        return self._life_time

    @life_time.setter
    def life_time(self, life_time):
        self._life_time = life_time

    @property
    def direction(self) -> vec:
        return self._direction
