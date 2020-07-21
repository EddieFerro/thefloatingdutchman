from pygame.math import Vector2 as vec
from thefloatingdutchman.objects.object_data import ObjectData


class BulletData(ObjectData):
    def __init__(self, direction: vec, life_time, spawn, vel, type5=False):
        super().__init__(life_time, spawn, vel)
        self._direction = direction
        self.type5 = type5

    @property
    def direction(self) -> vec:
        return self._direction
