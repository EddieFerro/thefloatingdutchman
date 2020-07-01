from abc import ABC, abstractmethod
from pygame.sprite import Sprite
from thefloatingdutchman.objects.object_data import ObjectData

class ObjectSprite(Sprite, ABC):

    def __init__(self, object_data: ObjectData):
        Sprite.__init__(self)
        self._data = object_data
        self._original_image = None
        self._set_original_image()
        self.image = self._original_image
        self.rect = self.image.get_rect()
        self.rect.center = object_data._pos

    @abstractmethod
    def _set_original_image(self):
        pass