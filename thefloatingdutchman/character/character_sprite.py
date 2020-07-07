from abc import ABC, abstractmethod

from pygame.sprite import Sprite
from pygame import sprite, surfarray
import numpy
import time

from thefloatingdutchman.character.character_data import CharacterData


class CharacterSprite(Sprite, ABC):

    def __init__(self, character_data: CharacterData):
        Sprite.__init__(self)
        self._data = character_data
        self._original_image = None
        self._angle = 0
        self._prev_shot = 0
        self._bullets = sprite.Group()
        self._set_original_image()  # defined by subclass
        self.image = self._original_image
        self.rect = self.image.get_rect()  # creates the rectangle
        self.rect.center = character_data.pos  # sets the spawn point

    @property
    def bullets(self):
        return self._bullets

    @abstractmethod
    def _set_original_image(self):
        pass

    def take_damage(self, damage: int):
        self._data.health = self._data.health - damage
        arr = surfarray.pixels3d(self.image)
        arr[:,:,0] = 255
        arr[:,:,1] = 0
        arr[:,:,2] = 0
        time.sleep(.020)
