from pygame.sprite import Sprite

from abc import ABC, abstractmethod

from character.character_data import CharacterData


class CharacterSprite(Sprite, ABC):

    def __init__(self, character_data: CharacterData):
        Sprite.__init__(self)
        self._data = character_data
        self._original_image = None
        self._set_original_image()  # defined by subclass
        self.image = self._original_image
        self.rect = self.image.get_rect()  # creates the rectangle
        self.rect.center = character_data.pos  # sets the spawn point

    @abstractmethod
    def _set_original_image(self):
        pass
