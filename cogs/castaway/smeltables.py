from . import world

class Copper(world.SmeltedResource):
    recipe = {
        world.Ore(world.OreType.COPPER)
    }


    def __init__(self):
        self.carriable = True
        self.stack_size = 10


class Bronze(world.SmeltedResource):
    recipe = {
        world.Ore(world.OreType.BRONZE)
    }

    
    def __init__(self):
        self.carriable = True
        self.stack_size = 10


class Iron(world.SmeltedResource):
    recipe = {
        world.Ore(world.OreType.IRON)
    }

    def __init__(self):
        self.carriable = True
        self.stack_size = 5