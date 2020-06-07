import character_sprite

class Character:
    def __init__(self, health):
        self.health = health 

    @property
    def health(self):
        return self._health
    
    @health.setter
    def health(self, health):
        self._health = health

    def _sprite_creation(self):
        print("Test")


class Player(Character):
    def __init__(self, health, fire_rate, spawnx, spawny, velx, vely):
        super().__init__(health)
        self.fire_rate = fire_rate
        self.velx = velx
        self.vely = vely
        self._spawnx = spawnx
        self._spawny = spawny
        self._sprite_creation()

    #setters and getters for fire rate
    @property
    def fire_rate(self):
        return self._fire_rate

    @fire_rate.setter
    def fire_rate(self, fire_rate):
        self._fire_rate = fire_rate
    
    #setters and getters for player velocity along the x axis
    @property
    def velx(self):
        return self._velx
    
    @velx.setter
    def velx(self, velx):
        self._velx = velx
    
    #setters and getters for player velocity along the y axis
    @property
    def vely(self):
        return self._vely
    
    @vely.setter
    def vely(self, vely):
        self._vely = vely
    
    #setters for the player's spawn point on the x axis and y axis
    @property
    def spawnx(self):
        return self._spawnx
    
    @property
    def spawny(self):
        return self._spawny
    
    #getter for player sprite
    @property
    def player_sprite(self):
        return self._player_sprite

    #creates player sprite
    def _sprite_creation(self):
        self._player_sprite = character_sprite.PlayerSprite(self._velx, self._vely, self._spawnx, self._spawny)


#enemy class can be later subclassed to create specific types of enemies, where some values might be more static
class Enemy(Character):
    def __init__(self, health, fire_rate, spawnx, spawny, velx, vely):
        super().__init__(health)
        self._fire_rate = fire_rate
        self._velx = velx
        self._vely = vely
        self._spawnx = spawnx
        self._spawny = spawny
        self._sprite_creation()

    #getters for fire rate
    @property
    def fire_rate(self):
        return self._fire_rate

    #getters for enemy velocity along the x axis
    @property
    def velx(self):
        return self._velx
    
    #getters for enemy velocity along the y axis
    @property
    def vely(self):
        return self._vely
        
    #setters for the enemy spawn point on the x axis and y axis
    @property
    def spawnx(self):
        return self._spawnx
    
    @property
    def spawny(self):
        return self._spawny
    
    @property
    def enemy_sprite(self):
        return self._enemy_sprite

    #creates enemy sprite
    def _sprite_creation(self):
        self._enemy_sprite = character_sprite.EnemySprite(self._velx, self._vely, self._spawnx, self._spawny)