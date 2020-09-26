from . import world
from . import smeltables


"""Wood Tools"""


class WoodAxe(world.CraftedResource):
    recipe = {world.Stick: 2, world.Wood: 3}

    name = "wood axe"

    def __init__(self):
        self.durability = 25


class WoodPickaxe(world.CraftedResource):
    recipe = {world.Stick: 2, world.Wood: 3}

    name = "wood pickaxe"

    def __init__(self):
        self.durability = 25


class WoodShovel(world.CraftedResource):
    recipe = {world.Stick: 2, world.Wood: 1}

    name = "wood shovel"

    def __init__(self):
        self.durability = 25


class WoodHoe(world.CraftedResource):
    recipe = {world.Stick: 2, world.Wood: 2}

    name = "wood hoe"

    def __init__(self):
        self.durability = 25


class WoodScythe(world.CraftedResource):
    recipe = {world.Stick: 3, world.Wood: 1}

    name = "wood scythe"

    def __init__(self):
        self.durability = 25


"""Copper Tools"""


class CopperAxe(world.CraftedResource):
    recipe = {smeltables.Copper: 3, world.Stick: 2}

    name = "copper axe"

    def __init__(self):
        self.durability = 50


class CopperPickaxe(world.CraftedResource):
    recipe = {smeltables.Copper: 3, world.Stick: 2}

    name = "copper pickaxe"

    def __init__(self):
        self.durability = 50


class CopperShovel(world.CraftedResource):
    recipe = {smeltables.Copper: 1, world.Stick: 2}

    name = "copper shovel"

    def __init__(self):
        self.durability = 50


class CopperHoe(world.CraftedResource):
    recipe = {smeltables.Copper: 2, world.Stick: 2}

    name = "copper hoe"

    def __init__(self):
        self.durability = 50


class CopperScythe(world.CraftedResource):
    recipe = {smeltables.Copper: 1, world.Stick: 3}

    name = "copper scythe"

    def __init__(self):
        self.durability = 50


"""Iron Tools"""


class IronAxe(world.CraftedResource):
    recipe = {smeltables.Iron: 3, world.Stick: 2}

    name = "iron axe"

    def __init__(self):
        self.durability = 100


class IronPickaxe(world.CraftedResource):
    recipe = {smeltables.Iron: 3, world.Stick: 2}

    name = "iron pickaxe"

    def __init__(self):
        self.durability = 100


class IronShovel(world.CraftedResource):
    recipe = {smeltables.Iron: 1, world.Stick: 2}

    name = "iron shovel"

    def __init__(self):
        self.durability = 100


class IronHoe(world.CraftedResource):
    recipe = {smeltables.Iron: 2, world.Stick: 2}

    name = "iron hoe"

    def __init__(self):
        self.durability = 100


class IronScythe(world.CraftedResource):
    recipe = {smeltables.Iron: 1, world.Stick: 3}

    name = "iron scythe"

    def __init__(self):
        self.durability = 100


"""Advanced Basic resources"""


class BundledLogs(world.CraftedResource):
    recipe = {world.Wood: 5}

    name = "bundled logs"


class String(world.CraftedResource):
    recipe = {world.PlantFiber: 5}

    name = "string"


class Rope(world.CraftedResource):
    recipe = {String: 25}

    name = "rope"

class Stick(world.CraftedResource):
    recipe = {world.Wood: 3}

    name = "stick"


"""End Game resources"""


class Sail(world.CraftedResource):
    recipe = {String: 50, Rope: 10}

    name = "sail"  # of will you fame


"""Buildings"""


class Workbench(world.CraftedResource):
    """Speeds up crafting for most tools and unlocks crafting late game items"""

    recipe = {world.Wood: 2}

    name = "workbench"

    def __init__(self):
        pass


class ToolBench(world.CraftedResource):
    recipe = {Workbench: 1, smeltables.Bronze: 8}

    name = "tool bench"

class Storage(world.CraftedResource):
    # recipe = {world.Wood: 25}

    name = "storage chest"

    def __init__(self):
        pass


class LargeStorage(world.CraftedResource):
    # recipe = {BundledLogs: 25, smeltables.Copper: 10}

    name = "large storage chest"

    def __init__(self):
        pass


class OreOven(world.CraftedResource):

    buildable = True
    recipe = {world.Rock: 20}

    name = "ore oven"

    def __init__(self):
        pass


"""
class WaterPurifier(world.CraftedResource):
    recipe = {world.Rock: 2, BundledLogs: 3, smeltables.Copper: 10}

    def __init__(self):
        pass
"""


class Hut(world.CraftedResource):
    recipe = {world.Wood: 25, Rope: 10, world.Leaves: 10, BundledLogs: 5, Storage: 1}

    buildable = True

    name = "hut"

    def __init__(self):
        pass


class UpgradedHut(world.CraftedResource):
    recipe = {
        BundledLogs: 25,
        smeltables.Iron: 10,
        world.Rock: 25,
        smeltables.Glass: 10,
        LargeStorage: 1,
    }

    buildable = True

    name = "better hut:tm:"

    def __init__(self):
        pass


class Firepit(world.CraftedResource):
    recipe = {world.Wood: 10, BundledLogs: 3, world.Leaves: 5}

    buildable = True

    name = "fire pit"

    def __init__(self):
        pass


class Boat(world.CraftedResource):
    recipe = {BundledLogs: 250, world.Wood: 250, Sail: 5, smeltables.Iron: 50}

    buildable = True

    name = "enormous boat"

    def __init__(self):
        pass


class Farm(world.CraftedResource):
    recipe = {world.Leaves: 25, world.Wood: 25, BundledLogs: 10}

    buildable = True

    name = "farm"

    def __init__(self):
        pass

"""
class Trap(world.CraftedResource):
    recipe = {world.Leaves: 25, world.Wood: 10, String: 25}

    def __init__(self):
        pass
"""
