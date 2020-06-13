import character_sprite
from abc import ABC, abstractmethod


class Character(ABC):
    def __init__(self, health, attack_speed, spawnx, spawny, vel):
        self._health = health
        self.attack_speed = attack_speed
        self._spawnx = spawnx
        self._spawny = spawny
        self._sprite = None
        self._sprite_creation(vel)

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

    # setters for the player's spawn point on the x axis and y axis
    @property
    def spawnx(self):
        return self._spawnx

    @property
    def spawny(self):
        return self._spawny

    @property
    def sprite(self):
        return self._sprite

    @abstractmethod
    def _sprite_creation(self, vel):
        pass


class Player(Character):
    def __init__(self, health, attack_speed, spawnx, spawny, vel):
        super().__init__(health, attack_speed, spawnx, spawny, vel)

    # creates player sprite

    def _sprite_creation(self, vel):
        self._sprite = character_sprite.PlayerSprite(
            self._spawnx, self._spawny, vel)


# enemy class can be later subclassed to create specific types of enemies
# where some values might be more static
class Enemy(Character):
    def __init__(self, health, attack_speed, spawnx, spawny, vel):
        super().__init__(health, attack_speed, spawnx, spawny, vel)

    # creates enemy sprite
    def _sprite_creation(self, vel):
        self._sprite = character_sprite.EnemySprite(self._spawnx, self._spawny, vel)
