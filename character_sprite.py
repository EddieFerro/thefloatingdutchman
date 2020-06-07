import pygame.sprite

class CharacterSprite(pygame.sprite.Sprite):
    
    def __init__(self, velx, vely, spawnx, spawny):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.Surface((50, 50)) #sets the size of the sprite
        self.image.fill((0,255,0)) #sets the color of the sprite, default green for visibility

        #self.image = pygame.image.load("").convert()  ---- this will be used later to import an image for a sprite

        self.rect = self.image.get_rect() #creates the rectangle
        self.rect.center = (spawnx, spawny) #sets the spawn point
        
        self._velx = velx #speed of movement along x axis
        self._vely = vely #speed of movement along y axis


class PlayerSprite(CharacterSprite):
    def __init__(self, velx, vely, spawnx, spawny):
        super().__init__(velx, vely, spawnx, spawny)

    #simple player movement
    def update(self):
        pressed = pygame.key.get_pressed()
        speed = 0
        if pressed[pygame.K_LEFT] or pressed[pygame.K_a]:
            speed = -self._velx
            self.rect.x += speed
        if pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
            speed = self._velx
            self.rect.x += speed
        if pressed[pygame.K_UP] or pressed[pygame.K_w]:
            speed = -self._vely
            self.rect.y += speed
        if pressed[pygame.K_DOWN] or pressed[pygame.K_s]:
            speed = self._vely
            self.rect.y += speed


class EnemySprite(CharacterSprite):
    def __init__(self, velx, vely, spawnx, spawny):
        super().__init__(velx, vely, spawnx, spawny)
    
    #Enemy AI might go in here
    #def update(self):
    