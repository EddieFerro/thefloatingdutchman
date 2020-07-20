from pygame.math import Vector2 as vec
from pygame import image
from thefloatingdutchman.objects.object_data import ObjectData


class BulletData(ObjectData):
    def __init__(self, direction: vec, life_time, spawn, vel, sprite: image):
        super().__init__(life_time, spawn, vel)
        self._sprite = sprite
        self._direction = direction

    @property
    def sprite(self) -> image:
        return self._sprite

    @property
    def direction(self) -> vec:
        return self._direction
