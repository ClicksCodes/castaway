from . import world

"""Wood Tools"""

class WoodAxe(world.CraftedResource):
    recipe = {
        world.Stick: 2,
        world.Wood: 3
    }

    def __init__(self):
        self.stack_size = 1
        self.durability = 25

class WoodPickaxe(world.CraftedResource):
    recipe = {
        world.Stick: 2,
        world.Wood: 3
    }

    def __init__(self):
        self.stack_size = 1
        self.durability = 25

class WoodShovel(world.CraftedResource):
    recipe = {
        world.Stick: 2,
        world.Wood: 1
    }

    def __init__(self):
        self.stack_size = 1
        self.durability = 25

class WoodHoe(world.CraftedResource):
    recipe = {
        world.Stick: 2,
        world.Wood: 2
    }

    def __init__(self):
        self.stack_size = 1
        self.durability = 25

class WoodScythe(world.CraftedResource):
    recipe = {
        world.Stick: 3,
        world.Wood: 1
    }

    def __init__(self):
        self.stack_size = 1
        self.durability = 25

"""Copper Tools"""

class CopperAxe(world.CraftedResource):
    recipe = {
        world.Copper: 3,
        world.Stick: 2
    }

    def __init__(self):
        self.stack_size = 1
        self.durability = 50

class CopperPickaxe(world.CraftedResource):
    recipe = {
        world.Copper: 3,
        world.Stick: 2
    }
    
    def __init__(self):
        self.stack_size = 1
        self.durability = 50

class CopperShovel(world.CraftedResource):
    recipe = {
        world.Copper: 1,
        world.Stick: 2
    }



"""Advanced Basic resources"""

class BundledLogs(world.CraftedResource):
    recipe = {
        world.Wood: 5
    }


"""Buildings"""

class Workbench(world.CraftedResource):
    """Speeds up crafting for most tools and unlocks crafting late game items"""
    recipe = {
        world.Wood:2
    }

    def __init__(self):
        pass

class Storage(world.CraftedResource):
    recipe = {
        world.Wood: 25
    }

    def __init__(self):
        pass

class LargeStorage(world.CraftedResource):
    recipe = {
        BundledLogs: 25,
        world.Copper: 10
    }
    def __init__(self):
        pass

class OreOven(world.CraftedResource):
    recipe = {
        world.Rock:20
    }

    def __init__(self):
        pass

class WaterPurifier(world.CraftedResource):
    recipe = {
        world.Rock: 2,
        BundledLogs: 3,
        world.Copper: 10
    }

    def __init__(self):
        pass

class Hut(world.CraftedResource):
    recipe = {
        world.Wood: 25,
        Rope: 10,
        world.Leaves: 10,
        BundledLogs: 5,
        Storage: 1
    }
    
    def __init__(self):
        pass

class UpgradedHut(world.CraftedResource):
    recipe = {
        BundledLogs: 25,
        world.Iron: 10,
        world.Rock: 25,
        Glass: 10,
        LargeStorage: 1
    }

    def __init__(self):
        pass

class Firepit(world.CraftedResource):
    recipe = {
        world.Wood: 10,
        BundledLogs: 3,
        world.Leaves: 5
    }

    def __init__(self):
        pass

class Boat(world.CraftedResource):
    recipe = {
        BundledLogs: 250,
        world.Wood: 250,
        Sail: 5,
        world.Iron: 50
    }
    
    def __init__(self):
        pass

class Farm(world.CraftedResource):
    recipe = {
        world.Leaves: 25,
        world.Wood: 25,
        BundledLogs: 10,
        String: 25
    }

    def __init__(self):
        pass

class Trap(world.CraftedResource):
    recipe = {
        world.Leaves: 25,
        world.Wood: 10,
        world.String: 25
    }

    def __init__(self):
        pass