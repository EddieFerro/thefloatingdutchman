from pygame import Vector2


class CharacterData():

    # expects spawn to be vector
    def __init__(self, health: int, attack_speed: int, spawn: Vector2, vel: int):
        self._health = health
        self._attack_speed = attack_speed
        self._pos = spawn
        self._vel = vel

    @property
    def health(self) -> int:
        return self._health

    @health.setter
    def health(self, health):
        self._health = health

    @property
    def attack_speed(self) -> int:
        return self._attack_speed

    @attack_speed.setter
    def attack_speed(self, attack_speed):
        self._attack_speed = attack_speed

    @property
    def pos(self) -> Vector2:
        return self._pos

    @pos.setter
    def pos(self, pos):
        self._pos = pos

    @property
    def vel(self) -> int:
        return self._vel

    @vel.setter
    def vel(self, new_vel: int) -> None:
        self._vel = new_vel
