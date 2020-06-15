from character.character_data import CharacterData


class PlayerData(CharacterData):
    def __init__(self, health, attack_speed, spawn, vel):
        super().__init__(health, attack_speed, spawn, vel)
