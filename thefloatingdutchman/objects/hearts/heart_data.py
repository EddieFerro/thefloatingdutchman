from thefloatingdutchman.objects.object_data import ObjectData


class HeartData(ObjectData):
    def __init__(self, life_time, spawn, vel):
        super().__init__(life_time, spawn, vel)
