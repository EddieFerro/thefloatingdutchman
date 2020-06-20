import math

from pygame import image, Rect, Surface, key, Vector2, mouse, transform
import pygame

from character.character_sprite import CharacterSprite
from character.player.player_data import PlayerData


class PlayerSprite(CharacterSprite):
    def __init__(self, player_data: PlayerData):
        super().__init__(player_data)

    def _set_original_image(self):
        sprite_sheet = image.load("topdown_sample.png").convert()

        # exact dimension of player sprite
        temp_rect = Rect((0, 0, 313, 207))
        self._original_image = Surface(temp_rect.size).convert()

        # sets image to a portion of spritesheet (surface)
        self._original_image.blit(sprite_sheet, (0, 0), temp_rect)

        # makes player appropriate size
        self._original_image = transform.scale(
            self._original_image, (int(313/4), int(207/4)))

    # simple player movement

    def update(self, screen):
        # TODO: Do we need this?
        # pygame.event.pump()
        self._calc_movement(screen)

    def _calc_movement(self, screen):
        x = 0
        y = 0

        keys = key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            x = -self._data.vel
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            x = self._data.vel
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            y = -self._data.vel
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            y = self._data.vel

        if x != 0 and y != 0:
            x *= 0.7071
            y *= 0.7071

        self._data.pos = self._data.pos + Vector2(x, y)

        # must be called in this order, considering fixing later
        self._calc_rotation()
        self._check_walls(screen)

    def _check_walls(self, screen):
        screen_rect = screen.get_rect()

        # stops rect from moving outside screen
        self.rect.clamp_ip(screen_rect)

        # repositions player at center of rect
        self._data.pos = Vector2(self.rect.center)

    def _calc_rotation(self):
        mouse_x, mouse_y = mouse.get_pos()
        rel_x, rel_y = mouse_x - self._data.pos.x, mouse_y - self._data.pos.y
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x) + 5
        self.image = transform.rotate(self._original_image, int(angle))
        self.rect = self.image.get_rect(center=self._data.pos)
        self.rect.center = self._data.pos
