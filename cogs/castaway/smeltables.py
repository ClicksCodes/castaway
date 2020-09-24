from . import world


class Copper(world.SmeltedResource):
    recipe = {world.Ore(world.OreType.COPPER): 1}
    name = "copper"
    def __init__(self):
        self.carriable = True
        self.stack_size = 10


class Bronze(world.SmeltedResource):
    recipe = {world.Ore(world.OreType.BRONZE): 1}
    name = "bronze"
    def __init__(self):
        self.carriable = True
        self.stack_size = 10


class Iron(world.SmeltedResource):
    recipe = {world.Ore(world.OreType.IRON): 1}
    name = "iron"
    def __init__(self):
        self.carriable = True
        self.stack_size = 5


class Glass(world.SmeltedResource):
    recipe = {world.Sand: 5}
    name = "glass"