import pygame.sprite
import math
from GameSettings import *
vector = pygame.math.Vector2

class CharacterSprite(pygame.sprite.Sprite):

    def __init__(self, spawnx, spawny):
        pygame.sprite.Sprite.__init__(self)

        self.original_image = pygame.Surface((20,50))
        self.original_image.fill(GREEN)
        self.image = pygame.Surface((20, 50))  # sets the size of the sprite
        self.image.fill(GREEN)  # sets the color of the sprite, default green for visibility

        # self.image = pygame.image.load("").convert()  ---- this will be used later to import an image for a sprite
        self.rect = self.image.get_rect()  # creates the rectangle
        self.rect.center = (spawnx, spawny)  # sets the spawn point
        self.pos = vector(spawnx, spawny)


class PlayerSprite(CharacterSprite):
    def __init__(self, spawnx, spawny):
        super().__init__(spawnx, spawny)
        # self.original_image = pygame.image.load("").convert()
        # self.original_image = pygame.transform.scale(self.original_image, (100, 100))
        # self.image = pygame.image.load("").convert()
        # self.image = pygame.transform.scale(self.image, (100, 100))

    def movement(self):
        self.velx = 0
        self.vely = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.velx = -PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.velx = PLAYER_SPEED
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.vely = -PLAYER_SPEED
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.vely =  PLAYER_SPEED
        self.fix_diag_move()
        self.vel = (self.velx, self.vely)

    def fix_diag_move(self):
        if self.velx != 0 and self.vely != 0:
            self.velx *= 0.7071
            self.vely *= 0.7071

    # simple player movement
    def update(self):
        pygame.event.pump()
        self.movement()
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.pos.x, mouse_y - self.pos.y
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        self.image = pygame.transform.rotate(self.original_image, int(angle))
        self.rect = self.image.get_rect(center=self.pos)
        self.pos += self.vel
        self.rect.center = self.pos

class EnemySprite(CharacterSprite):
    def __init__(self, spawnx, spawny):
        super().__init__(spawnx, spawny)

    # Enemy AI might go in here
    # def update(self):
