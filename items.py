"""

x: Basic items, used in most recipes, cannot be crafted
1x: ores/metals
2x-3x: Materials, can be crafted, main components of structures
4x: Foodstuffs
5x-6x: Structures

"""

items = {
    0: {
        "name": "wood",
        "description": "Basic wood, used to make planks and tools",
        "found": "Scavenging"
    },
    1: {
        "name": "leaves",
        "description": "Leaves found on trees, could make a nice shelter",
        "found": "Scavenging"
    },
    2: {
        "name": "rock",
        "description": "A small rock!",
        "found": "Scavenging"
    },
    3: {
        "name": "sand",
        "description": "Could make a nice window, or somewhat purify water",
        "found": "Scavenging"
    },
    4: {
        "name": "water",
        "description": "Just your basic H₂O",
        "found": "Purifying water"
    },
    5: {
        "name": "dirty water",
        "description": "Water, but dirty - Make sure to purify it",
        "found": "Not possible"
    },
    10: {
        "name": "coal",
        "description": "Used to make heat, make sure it is in steady supply",
        "found": "Mining"
    },
    11: {
        "name": "gold",
        "description": "GOLD! ALWAYS BELIEVE IN YOUR SOUL",
        "found": "Mining"
    },
    12: {
        "name": "silver",
        "description": "Silver:tm: - Because you got second place",
        "found": "Mining"
    },
    13: {
        "name": "iron",
        "description": "Used to make tools mainly",
        "found": "Mining"
    },
    20: {
        "name": "planks",
        "description": "Wooden planks, used for most recipes - a plank of wood",
        "found": "Crafting",
        "recipe": {
            "in": {
                0: 1
            },
            "out": 2,
            "time": 1
        }
    },
    21: {
        "name": "sticks",
        "description": "Sticks to hold something up",
        "found": "Crafting",
        "recipe": {
            "in": {
                20: 1
            },
            "out": 2,
            "time": 1
        }
    },
    22: {
        "name": "flint",
        "description": "Flint for a flint and steel",
        "found": "Crafting",
        "recipe": {
            "in": {
                13: 2
            },
            "out": 1,
            "time": 30
        }
    },
    23: {
        "name": "flint and steel",
        "description": "Lights a fire",
        "found": "Crafting",
        "recipe": {
            "in": {
                13: 1,
                22: 1
            },
            "out": 1,
            "time": 1
        }
    },
    40: {
        "name": "fish",
        "description": "* Not suitable for vegetarians",
        "found": "Fishing"
    },
    401: {
        "name": "cooked fish",
        "description": "* Not suitable for vegetarians - Even when cooked",
        "found": "Cooking"
    },
    41: {
        "name": "berries",
        "description": "Berries! Not poisonous",
        "found": "Farming"
    },
    42: {
        "name": "coconuts",
        "description": "Suitable for food and drink",
        "found": "Farming"
    },
    43: {
        "name": "chicken",
        "description": "Make sure to cook it, you'll lose a lot of health",
        "found": "Farming"
    },
    431: {
        "name": "cooked chicken",
        "description": "You cooked it, well done",
        "found": "Cooking"
    },
    44: {
        "name": "insects",
        "description": "While technically edible, make sure to kill them",
        "found": "Farming"
    },
    45: {
        "name": "bananas",
        "description": "A group of bananas is called a hand",
        "found": "Farming"
    },
    46: {
        "name": "egg",
        "description": "Just an egg, y'know",
        "found": "Farming"
    },
    461: {
        "name": "cooked egg",
        "description": "Just an egg, y'know",
        "found": "Cooking"
    },
    47: {
        "name": "seaweed",
        "description": "Weed, from the sea",
        "found": "Farming"
    },
    471: {
        "name": "cooked seaweed",
        "description": "Weed, from the sea",
        "found": "Cooking"
    },
    48: {
        "name": "mushrooms",
        "description": "Gotta get some shrooms",
        "found": "Farming"
    },
    481: {
        "name": "cooked mushrooms",
        "description": "Gotta get some shrooms",
        "found": "Cooking"
    },
    49: {
        "name": "nuts",
        "description": "NUT",
        "found": "Farming"
    },
    50: {
        "name": "store upgrade",
        "description": "Gives your community store more capacity",
        "found": "Crafting",
        "recipe": {
            "in": {
                0: 50,
                2: 5
            },
            "out": 1,
            "max": 1,
            "time": 60
        }
    },
    51: {
        "name": "campfire",
        "description": "Makes your island visible to other online islands",
        "found": "Crafting",
        "recipe": {
            "in": {
                0: 50,
                1: 50,
                2: 10,
                21: 25
            },
            "out": 1,
            "max": 1,
            "time": 60 * 60 * 5
        }
    }
}


class Multiplier:
    def __init__(self, item, level=1, skill=0):
        self.item = item
        self.level = level
        self.skill = skill + 1

    def itemMultiplier(self):
        if int(self.item) == 50:
            return round((int(self.level)**2) / self.skill, 2)
        else:
            return round(1 / self.skill, 3)

    def timeMultiplier(self):
        if int(self.item) == 50:
            return round(((int(self.level)**2) * 2) / self.skill, 3)
        else:
            return round(1 / self.skill, 3)
