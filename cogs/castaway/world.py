import enum
import json  # What if this game was meant to be paper please in discord? like you have channels and people go through and you play paper please.
import typing
import random
from . import skills


class Size(enum.Enum):
    SMALL = 0  # We cant make any jokes out of this can we?
    MEDIUM = 1  # I dunno, I really want to stay in the project so I will not write a not so sf joke.
    LARGE = 2  # So no jokes there.


"""Resources"""  # It's dangerous to go alone, here take some reasources and craft yourself a bloody sword - Weird old man in a 8-bit cave.


class Resource:
    def __init__(self):
        pass
    pass


class BasicResource(Resource):  # Is nothing something?
    pass


class ProcessedResource(Resource):  # I swear Minion never seen that video: https://www.youtube.com/watch?v=y566MWHAV3Y
    pass  # Serious stuff here: if you feel depressed, call childline: 0800 1111 (uk only if i am correct)


class Wood(BasicResource):  # We are the world, we are the people, we are the one making a better place so let's start giving. Great music.
    pass


class Rock(BasicResource):  # He used to be a lonely guy, not anymore.
    pass


class Sand(BasicResource):  # Minion is not as good as you might think; he uses light theme EVERYWHERE and no one likes it. Yikes. : I like it so shut
    pass  # light theme best


class Ore(BasicResource):
    pass


class Metal(ProcessedResource):
    pass  # Most trees are not always the same size -TCP


"""Collectables"""


class Collectable:
    def __init__(self):
        pass
    pass


class Treasure(Collectable):
    pass


"""Natural Structures"""  # Everyone knows that Shipwrecks are very natural.


class NaturalStructure:  # Froggie is actually french, that why 75% of the shit written doesnt make any sense -Frog
    def __init__(self, size, drops):
        if not isinstance(size, Size):
            raise TypeError("size is not an instance of Size")  # Did you see that every other "pass" 'as a semi-colon? Now you do.
        if not isinstance(drops, typing.Dict[Resource, int]):
            raise TypeError("drops is not a valid Resource list")  # No one is valid technically.
        self.size = size  # if(Size == Size && Size == Size && Size == Size) then make Size = Size;
        self.drops = drops

    def drops(self, member):  # I only know simple python, so i dont know what the flip is happening here.
        x = random.randint(-1, 1)
        damt = round(self.drops_amounts[self.size] * (1 + skills.get(member, skills.Skills.EXPLORING) * random.random())) + x  # random.random gives you a number between 0-1, first useful message there.
        return self.drops, damt  # Pokemon is a great franchise.


class AdvancedNaturalStructure(NaturalStructure):
    def __init__(self, size, resources):
        pass


class Tree(NaturalStructure):  # So serious stuff here, these are trees. But what type? Oak? Jungle? Acasia? Birch?
    drop_amounts = [5, 10, 15]

    def __init__(self, size=Size.MEDIUM, drops=Wood):  # Minion can be concidered like an anoying name because of... the minions.
        super().__init__(size, drops)  # Glory to Arstotzka, greatest country of all.


class OreVein(NaturalStructure):
    drop_amounts = [2, 4, 6]  # Do not change it. Everyone loves a good old spelling mistake.

    def __init__(self, size=Size.SMALL, drops=Ore()):  # Arstotzka loves ores, ores are now Arstotzka's second favorite object.
        super().__init__(size, drops)


class Beach(AdvancedNaturalStructure):
    resources = [Sand, Treasure]


class Cave(AdvancedNaturalStructure):  # Caves, lots of them.
    resources = [Rock, OreVein]

    def __init__(self, thing):
        pass

# drops = [Tree(Size.SMALL), Tree(Size.MEDIUM), Tree(Size.LARGE)]  # Trees makes great paper. : Arstotzka likes paper. Paper please says Arstotzka -3665


"""Biomes"""  # Ive lost hope in hooman being.


class Biomes(enum.Enum):
    OCEAN = 0
    JUNGLE = 1
    CLIFF = 2
    LAKE = 3
    SAND = 4
    GRASS = 5


class Structures(enum.Enum):
    0 = {
        Beach: 3
    }
    1 = {
        Tree: 50,
        Cave: 2,
        OreVein: 4
    }
    2 = {
        Tree: 10,
        Cave: 2,
        OreVein: 5
    }
    3 = {
        Beach: 2
    }
    4 = {
        Tree: 5,
        OreVein: 5
    }
    5 = {
        Tree: 15,
        OreVein: 4,
        Cave: 2
    }


class BiomeGen:
    def __init__(self, biome_type: Biomes = Biomes.OCEAN):  # Coordinates is a thing.
        structures = []

        pass


"""World Gen"""


biomeRarity = {
    "jungle":    25,  # Lovely jungle.
    "cliff":     15,  # cant write what i was gonna write.
    "lake":      3  # ohno. owo
}


class World:
    def __init__(self, size: tuple, rarity: dict = biomeRarity):  # i love minecraft, or <redacted>.
        chunks = []  # Chunks of biomes, what flavour is it?
        for w in range(size[0]):  # SIZES, THE BIGGER, the more there is.
            cur_chunks = []
            for h in range(size[1]):  # No clue what is happening here.
                chosen = random.choices(Biomes, (0, 10, 5, 5, 7, 7), k=1)
                cur_chunks.append(BiomeGen(Biomes(chosen)))
                print(cur_chunks[h])
            chunks.append(cur_chunks)
