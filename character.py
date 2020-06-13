import character_sprite
from abc import ABC, abstractmethod


class Character(ABC):
    def __init__(self, health, attack_speed, spawnx, spawny, velx, vely):
        self._health = health
        self.attack_speed = attack_speed
        self.velx = velx
        self.vely = vely
        self._spawnx = spawnx
        self._spawny = spawny
        self._sprite = None
        self._sprite_creation()

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

    # setters and getters for player velocity along the x axis
    @property
    def velx(self):
        return self._velx

    @velx.setter
    def velx(self, velx):
        self._velx = velx

    # setters and getters for player velocity along the y axis
    @property
    def vely(self):
        return self._vely

    @vely.setter
    def vely(self, vely):
        self._vely = vely

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
    def _sprite_creation(self):
        pass


class Player(Character):
    def __init__(self, health, attack_speed, spawnx, spawny, velx, vely):
        super().__init__(health, attack_speed, spawnx, spawny, velx, vely)

    # creates player sprite

    def _sprite_creation(self):
        self._sprite = character_sprite.PlayerSprite(self.velx, self.vely, self._spawnx, self._spawny)


# enemy class can be later subclassed to create specific types of enemies
# where some values might be more static
class Enemy(Character):
    def __init__(self, health, attack_speed, spawnx, spawny, velx, vely):
        super().__init__(health, attack_speed, spawnx, spawny, velx, vely)

    # creates enemy sprite
    def _sprite_creation(self):
        self._sprite = character_sprite.EnemySprite(self.velx, self.vely, self._spawnx, self._spawny)
