import pygame.sprite
import math
import pygame
from GameSettings import GREEN, PLAYER_SPEED
from pygame.math import Vector2



class CharacterSprite(pygame.sprite.Sprite):

    def __init__(self, velx, vely, spawnx, spawny):
        pygame.sprite.Sprite.__init__(self)
        self.pos = Vector2(spawnx, spawny)

        self._velx = velx
        self._vely = vely


class PlayerSprite(CharacterSprite):
    def __init__(self, spawnx, spawny):
        super().__init__(spawnx, spawny)
        ss = pygame.image.load("topdown_sample.png").convert()

        # exact dimension of player sprite
        self.rect = pygame.Rect((0, 0, 313, 207))
        self.image = pygame.Surface(self.rect.size).convert()

        # sets image to a portion of spritesheet (surface)
        self.image.blit(ss, (0, 0), self.rect)

        # makes player appropriate size
        self.image = pygame.transform.scale(
            self.image, (int(313/4), int(207/4)))

        self.original_image = self.image

    # simple player movement
    def update(self):
        pygame.event.pump()
        self.calc_movement()

    def calc_movement(self):
        x = 0
        y = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            x = -PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            x = PLAYER_SPEED
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            y = -PLAYER_SPEED
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            y = PLAYER_SPEED

        if x != 0 and y != 0:
            x *= 0.7071
            y *= 0.7071

        self.vel = Vector2(x, y)
        self.pos += self.vel
        self.calc_rotation()

    def calc_rotation(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.pos.x, mouse_y - self.pos.y
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x) + 5
        self.image = pygame.transform.rotate(self.original_image, int(angle))
        self.rect = self.image.get_rect(center=self.pos)
        self.rect.center = self.pos
 


class EnemySprite(CharacterSprite):
    def __init__(self, spawnx, spawny):
        super().__init__(spawnx, spawny)
        self.original_image = pygame.Surface((20, 50))
        self.original_image.fill(GREEN)
        self.image = self.original_image

        self.rect = self.image.get_rect()  # creates the rectangle
        self.rect.center = (spawnx, spawny)  # sets the spawn point

    # Enemy AI might go in here
    def update(self, players, enemies):
        direction_vector = pygame.math.Vector2(- self.rect.x +players.rect.x, - self.rect.y + players.rect.y)
        try:
            direction_vector.scale_to_length(self._velx)
            if self.rect.colliderect(players.rect):
                enemies.remove(self)
            self.rect.move_ip(direction_vector)
        except ValueError:
            return
