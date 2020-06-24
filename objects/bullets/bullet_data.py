from pygame.math import Vector2 as vec
from objects.object_data import ObjectData

class BulletData(ObjectData):
    def __init__(self, damage: int, direction : vec, life_time, spawn, vel):
        super().__init__(life_time, spawn, vel)
        self._damage = damage
        self._direction = direction
    
    @property
    def damage(self) -> int:
        return self._damage

    @property
    def direction(self) -> vec:
        return self._direction