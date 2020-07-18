from pygame import Vector2

from thefloatingdutchman.character.character_data import CharacterData


class EnemyData(CharacterData):
    """Enemy class for base enemy can be later subclassed to create specific types of enemies """
    # Will make sure to subclass enemy types later on

    def __init__(self, health: int, attack_speed: int, spawn: Vector2, vel, level):
        super().__init__(health, attack_speed, spawn, vel)
        self._stopMoving = False
