


class baseObject():
    def __init__(self, pos, vel):
        self.pos = pos
        self.vel = vel


    def update(self, detlaTime):
        pass

    def draw(self, window):
        pass

    def add_force(self, forceVec):
        pass


class Fish(baseObject):
    def __init__(self, pos, vel):
        super.__init__(pos, vel)
        pass


class Treasure(baseObject):
    def __init__(self, pos, vel):
        super.__init__(pos, vel)
        pass