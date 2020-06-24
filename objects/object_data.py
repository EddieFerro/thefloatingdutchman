from pygame import Vector2 as vec

class ObjectData:

    def __init__(self, life_time: int, pos: vec, vel: int):
        self._life_time = life_time
        self._pos = pos
        self._vel = vel
    
    @property
    def life_time(self) -> int:
        return self._life_time
    
    @life_time.setter
    def life_time(self, life_time):
        self._life_time = life_time
    
    @property
    def pos(self) -> vec:
        return self._pos
    
    @pos.setter
    def pos(self, pos):
        self._pos = pos
    
    @property
    def vel(self) ->int:
        return self._vel