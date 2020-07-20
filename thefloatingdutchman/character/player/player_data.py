from thefloatingdutchman.character.character_data import CharacterData


class PlayerData(CharacterData):
    def __init__(self, health, attack_speed, spawn, vel):
        super().__init__(health, attack_speed, spawn, vel)
        self._max_health = 4

    def gain_health(self, healing: int):
        self.health = min(self.health + 1, self._max_health)
