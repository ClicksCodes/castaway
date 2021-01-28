"""Base materials"""

class Wood:
    iid = 0
    name = "wood"
    description = "Basic wood, used to make planks and tools"
    stack_size = 32
    def __init__(self):
        pass

class Leaves:
    iid = 1
    name = "leaves"
    description = "Leaves found from trees, could make a nice shelter"
    stack_size = 32
    def __init__(self):
        pass

class Stone:
    iid = 2
    name = "stone"
    description = "Solid rock used in construction"
    stack_size = 32
    def __init__(self):
        pass

class Sand:
    iid = 3
    name = "sand"
    description = "Could make a nice window, or somewhat purify water"
    stack_size = 32
    def __init__(self):
        pass

class water:
    iid = 4
    name = "water"
    description = "Just your basic H₂O"
    stack_size = 10
    def __init__(self, cleanliness=0):
        self.cleanliness = cleanliness

class Coal:
    iid = 5
    name = "coal"
    description = "Used to make heat, make sure it is in steady supply"
    stack_size = 32
    def __init__(self):
        pass

class Gold: 
    pass
class Silver: 
    pass
class Platinum: 
    pass
class Copper: 
    pass
class Iron: 
    pass
class Copper: 
    pass
class Bronze: 
    pass