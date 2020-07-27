from pygame import Vector2 as vec


class ObjectData:
    def __init__(self, pos: vec, vel: int):
        self._pos = pos
        self._vel = vel

    @property
    def pos(self) -> vec:
        return self._pos

    @pos.setter
    def pos(self, pos):
        self._pos = pos

    @property
    def vel(self) -> int:
        return self._vel
