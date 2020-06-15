from character.character_data import CharacterData


class EnemyData(CharacterData):
    """Enemy class for base enemy can be later subclassed to create specific types of enemies """

    def __init__(self, health, attack_speed, spawn, vel):
        super().__init__(health, attack_speed, spawn, vel)
