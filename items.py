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
        "stackSize": 32,
        "description": "Basic wood, used to make planks and tools"
    },
    1: {
        "name": "leaves",
        "stackSize": 32,
        "description": "Leaves found on trees, could make a nice shelter"
    },
    2: {
        "name": "rock",
        "stackSize": 32,
        "description": "A small rock!"
    },
    3: {
        "name": "sand",
        "stackSize": 32,
        "description": "Could make a nice window, or somewhat purify water"
    },
    4: {
        "name": "water",
        "stackSize": 10,
        "description": "Just your basic H₂O",
        "props": ["cleanliness"]
    },
    5: {},
    6: {},
    7: {},
    8: {},
    9: {},
    10: {
        "name": "coal",
        "description": "Used to make heat, make sure it is in steady supply",
        "stackSize": 32
    },
    11: {
        "name": "gold",
        "description": "GOLD! ALWAYS BELIEVE IN YOUR SOUL",
        "stackSize": 32
    },
    12: {
        "name": "silver",
        "description": "Silver:tm: - Because you got second place",
        "stackSize": 32
    },
    13: {
        "name": "iron",
        "description": "Used to make tools mainly",
        "stackSize": 32
    },
    14: {},
    15: {},
    16: {},
    17: {},
    18: {},
    19: {},
    20: {},
    21: {},
    22: {},
    23: {},
    24: {},
    25: {},
    26: {},
    27: {},
    28: {},
    29: {},
    30: {},
    31: {},
    32: {},
    33: {},
    34: {},
    35: {},
    36: {},
    37: {},
    38: {},
    39: {},
    40: {
        "name": "fish",
        "description": "* Not suitable for vegetarians",
        "stackSize": 10
    },
    401: {
        "name": "cooked fish",
        "description": "* Not suitable for vegetarians - Even when cooked",
        "stackSize": 10
    },
    41: {
        "name": "berries",
        "description": "Berries! Not poisonous",
        "stackSize": 10
    },
    42: {
        "name": "coconuts",
        "description": "Suitable for food and drink",
        "stackSize": 10
    },
    43: {
        "name": "chicken",
        "description": "Make sure to cook it, you'll lose a lot of health",
        "stackSize": 10
    },
    431: {
        "name": "cooked chicken",
        "description": "You cooked it, well done",
        "stackSize": 10
    },
    44: {
        "name": "insects",
        "description": "While technically edible, make sure to kill them",
        "stackSize": 10
    },
    45: {
        "name": "bananas",
        "description": "A group of bananas is called a hand",
        "stackSize": 10
    },
    46: {
        "name": "egg",
        "description": "Just an egg, y'know",
        "stackSize": 10
    },
    461: {
        "name": "cooked egg",
        "description": "Just an egg, y'know",
        "stackSize": 10
    },
    47: {
        "name": "seaweed",
        "description": "Weed, from the sea",
        "stackSize": 10
    },
    471: {
        "name": "cooked seaweed",
        "description": "Weed, from the sea",
        "stackSize": 10
    },
    48: {
        "name": "mushrooms",
        "description": "Gotta get some shrooms",
        "stackSize": 10
    },
    481: {
        "name": "cooked mushrooms",
        "description": "Gotta get some shrooms",
        "stackSize": 10
    },
    49: {
        "name": "nuts",
        "description": "NUT",
        "stackSize": 10
    }
}
