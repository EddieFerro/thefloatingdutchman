import character_sprite
from abc import ABC, abstractmethod


class Character(ABC):

    # expects spawn to be vector
    def __init__(self, health, attack_speed, spawn, vel):
        self._health = health
        self.attack_speed = attack_speed
        self._sprite = None
        self._sprite_creation(spawn, vel)

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, health):
        self._health = health

    @property
    def attack_speed(self):
        return self._attack_speed

    @attack_speed.setter
    def attack_speed(self, attack_speed):
        self._attack_speed = attack_speed

    @property
    def sprite(self):
        return self._sprite

    @abstractmethod
    def _sprite_creation(self, vel, spawn):
        pass


class Player(Character):
    def __init__(self, health, attack_speed, spawn, vel):
        super().__init__(health, attack_speed, spawn, vel)

    # creates player sprite

    def _sprite_creation(self, spawn, vel):
        self._sprite = character_sprite.PlayerSprite(spawn, vel)



# enemy class can be later subclassed to create specific types of enemies
# where some values might be more static
class Enemy(Character):
    def __init__(self, health, attack_speed, spawn, vel):
        super().__init__(health, attack_speed, spawn, vel)

    # creates enemy sprite
    def _sprite_creation(self, spawn, vel):
        self._sprite = character_sprite.EnemySprite(spawn, vel)

