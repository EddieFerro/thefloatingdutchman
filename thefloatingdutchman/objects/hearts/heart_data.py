from thefloatingdutchman.objects.object_data import ObjectData


class HeartData(ObjectData):
    def __init__(self, spawn, vel):
        super().__init__(spawn, vel)
