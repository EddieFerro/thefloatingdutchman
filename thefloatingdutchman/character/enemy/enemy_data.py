from thefloatingdutchman.character.character_data import CharacterData
import random


class EnemyData(CharacterData):
    """Enemy class for base enemy can be later subclassed to create specific types of enemies """
    # Will make sure to subclass enemy types later on
    def __init__(self, health, attack_speed, spawn, vel):
        super().__init__(health, attack_speed, spawn, vel)
        self._type2 = random.choices([True,False], weights=[0.2, 0.8], k = 1)[0]
        self._stopMoving = False

