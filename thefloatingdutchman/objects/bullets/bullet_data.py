from pygame.math import Vector2 as vec
from pygame import image
from thefloatingdutchman.objects.object_data import ObjectData


class BulletData(ObjectData):
    def __init__(self, direction: vec, life_time, spawn, vel, type5=False, sprite: image):

        super().__init__(life_time, spawn, vel)
        self._sprite = sprite
        self._direction = direction
        self.type5 = type5

    @property
    def sprite(self) -> image:
        return self._sprite

    @property
    def direction(self) -> vec:
        return self._direction
