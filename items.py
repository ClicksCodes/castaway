"""

x: Basic items, used in most recipes, cannot be crafted
1x: reserved for ores/metals
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
    40: {
        "name": "fish",
        "description": "* Not suitable for vegetarians",
        "stackSize": 10,
        "props": ["cooked", "type"]
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
        "stackSize": 10,
        "props": ["cooked"]
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
        "stackSize": 10,
        "props": ["preparation"]
    },
    47: {
        "name": "seaweed",
        "description": "Weed, from the sea",
        "stackSize": 10,
        "props": ["cooked"]
    },
    48: {
        "name": "mushrooms",
        "description": "Gotta get some shrooms",
        "stackSize": 10,
        "props": ["cooked"]
    },
    49: {
        "name": "nuts",
        "description": "NUT",
        "stackSize": 10
    }
}
