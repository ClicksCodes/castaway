import enum  # Enums are fun, you know coroutines and stuff. (it's not)
import json  # What if this game was meant to be paper please in discord? like you have channels and people go through and you play paper please.
import typing  # Why would you need typing if you are already typing code?
import random  # BEST IMPORT.
from . import skills  # Skills. lovely.


class Size(enum.Enum):  # So if enums are not for coroutines, what are they for?
    SMALL = 0  # We cant make any jokes out of this can we?
    MEDIUM = 1  # I dunno, I really want to stay in the project so I will not write a not so sf joke.
    LARGE = 2  # So no jokes there.


"""Resources"""  # It's dangerous to go alone, here take some reasources and craft yourself a bloody sword - Weird old man in a 8-bit cave.


class ProcessTypes(enum.Enum):
    SMELTABLE = 0
    COOKABLE = 1
    CRAFTABLE = 2


class OreType(enum.Enum):
    COPPER = 0
    BRONZE = 1
    IRON = 2
    GOLD = 3


"""Resource types"""


class Resource:  # So enums if "set of options"?
    def __init__(self):  # i have no clue what it is for.
        self.carriable: bool
        self.stack_size: int


class BasicResource(Resource):  # Is nothing something?
    pass  # I'll PASS on that.


class ProcessedResource(
    Resource
):  # I swear Minion never seen that video: https://www.youtube.com/watch?v=y566MWHAV3Y
    def __init__(self, type):
        self.process_type: ProcessTypes | None

    # Serious stuff here: if you feel depressed, call childline: 0800 1111 (uk only if i am correct)


class CraftedResource(ProcessedResource):
    def __init__(self):
        super().__init__(process_type=ProcessTypes.CRAFTABLE)


class SmeltedResource(ProcessedResource):
    def __init__(self):
        super().__init__(process_type=ProcessTypes.SMELTABLE)


"""Basic Resources"""


class Wood(
    BasicResource
):  # We are the world, we are the people, we are the one making a better place so let's start giving. Great music.

    name = "wood"

    def __init__(self):
        self.stack_size = 50
        self.carriable = True


class Rock(BasicResource):  # He used to be a lonely guy, not anymore.
    name = "rock"
    def __init__(self):
        self.stack_size = 10
        self.carriable = True


class Sand(
    BasicResource
):  # Minion is not as good as you might think; he uses light theme EVERYWHERE and no one likes it. Yikes. : I like it so shut
    def __init(self):  # light theme best : aint no way that's true -TCP
        self.stack_size = 10
        self.carriable = False


class Stick(BasicResource):

    name = "stick"

    def __init__(self):
        self.gives = 1


class PlantFiber(BasicResource):
    name = "plantfiber"
    def __init__(self):
        self.gives = 1


class Leaves(BasicResource):
    
    name = "leaves"

    def __init__(self):
        self.gives = 1


"""Metal"""


class Ore(BasicResource):
    def __init__(self, oretype: OreType = OreType.COPPER):
        self.stack_size = 5
        self.carriable = True
        self.ore_type = oretype


"""Collectables"""


class Collectable:
    def __init__(
        self,
    ):  # isnt this script a bit too long? like it really feels like YandereDev code but looks nicer and all but
        pass  # Extremely long, wouldnt it impact on performance?


class Treasure(Collectable):  # Im gonna have fun when this is going to be finished.
    pass


"""Natural Structures"""  # Everyone knows that Shipwrecks are very natural.


class NaturalStructure:  # Froggie is actually french, that why 75% of the shit written doesnt make any sense -Frog
    def __init__(self, size, drops):
        if not isinstance(size, Size):
            raise TypeError(
                "size is not an instance of Size"
            )  # Did you see that every other "pass" 'as a semi-colon? Now you do.
        if not isinstance(drops, typing.Dict[Resource, int]):
            raise TypeError(
                "drops is not a valid Resource list"
            )  # No one is valid technically.
        self.size = size  # if(Size == Size && Size == Size && Size == Size) then make Size = Size;
        self.drops = drops

    def drop(self, member):
        # I only know simple python, so i dont know what the flip is happening here.
        x = random.randint(-1, 1)
        damt = (
            round(
                self.drops_amounts[self.size]
                * (
                    1 + skills.get(member, skills.Skills.EXPLORING) * random.random()
                )  # In reality, I am a slave and a test player... or not.
            )
            + x
        )  # random.random gives you a number between 0-1, first useful message there.
        return self.drops, damt  # Pokemon is a great franchise.


class AdvancedNaturalStructure(NaturalStructure):
    def __init__(
        self, size, resources
    ):  # If this is going to be PayToWin, im taking 50% of the
        pass


class Tree(NaturalStructure):  # Most trees are not always the same size -TCP
    # So serious stuff here, these are trees. But what type? Oak? Jungle? Acasia? Birch? : They're of the tree variety -TCP
    drop_amounts = [5, 10, 15]

    def __init__(self, size=Size.MEDIUM, drops=Wood):
        # Minion can be concidered like an anoying name because of... the minions.
        super().__init__(size, drops)  # Glory to Arstotzka, greatest country of all.


class OreVein(NaturalStructure):
    drop_amounts = [
        2,
        4,
        6,
    ]  # Do not change it. Everyone loves a good old spelling mistake.

    def __init__(
        self, size=Size.SMALL, drops=Ore(OreType.COPPER)
    ):  # Arstotzka loves ores, ores are now Arstotzka's second favorite object.
        super().__init__(size, drops)


class Beach(AdvancedNaturalStructure):  # oh structures?
    resources = [Sand, Treasure]  # Treasures in sand -- originality.


class Cave(AdvancedNaturalStructure):  # Caves, lots of them.
    resources = [
        Rock,
        OreVein,
    ]  # Veins are everywhere, deep inside the earth to inside your body -- blood veins.

    def __init__(self, thing):  # stuff working by itself?
        pass  # Pass it on.


# drops = [Tree(Size.SMALL), Tree(Size.MEDIUM), Tree(Size.LARGE)]  # Trees makes great paper. : Arstotzka likes paper. Paper please says Arstotzka -3665


"""Biomes"""  # Ive lost hope in hooman being.


class Biomes(
    enum.Enum
):  # I am writing this down to up so things might get weird, sentence wise.
    OCEAN = 0  # Anything after this is going or is already unreadable as it doesnt make sense:
    JUNGLE = 1  # Never been into a jungle but, after reading the jungle book, it doesnt really change any opinions on if you would go into a jungle.
    CLIFF = 2  # Cliffs are also nice, you can see a lot.
    LAKE = 3  # On the other hand, lakes. Best thing ever. you dont get dirty, +10 if it as pebbles.
    SAND = 4  # Sand is just annoying, like you go to the beach, you go into the water and, YOU HAVE SAND EVERYWHERE!
    GRASS = 5  # Anyone used to put grass in their cereals? i used to for some dark and unknown reasons.


biome_structures = {  # These are not worth commenting
    0: {  # Just look at them,
        Beach: 3,  # I really have no idea what to write here.
        None: 97,
    },  # Useless, only holding code together,
    1: {  # Doing nothing else,
        Tree: 50,  # I mean, there is plenty of space and all,
        Cave: 2,  # But you know, there isnt much we can write,
        OreVein: 4,  # We could talk about the oreVeins,
        None: 44,
    },  # just holdin'
    2: {  # and holdin'
        Tree: 10,  # Or the trees and how they'll gonna work,
        Cave: 2,  # But that is just plain boring,
        OreVein: 5,  # Actually, why is oreVeins twice here?
        None: 83,
    },  # Still doing the same job
    3: {Beach: 2, None: 98},  # and here too!  # And beach?  # Guess what? here too.
    4: {  # aaaand here.
        Tree: 5,  # And trees?
        OreVein: 5,  # Must be normal, or is it?
        None: 90,
    },  # Minion love them.
    5: {  # here too.
        Tree: 15,  # AND SOME MORE TREES HERE!!
        OreVein: 4,  # I really dont understand why,
        Cave: 2,  # Maybe if i were to read the code...
        None: 79,
    },  # im not even bothered putting caps anymore.
}  # like i am not paid for this, and for the best. : What if you were @slave? -TCP : That would be fantastic - slave : How much would you like? -TCP : 3 quid an hour is good enough really. - slave : It shall be done -TCP : Here is my paypal.me: https://paypal.me/thefroggie85/
# hour 1 @slave, start working -TCP : ok 2nd in charge officer.


class Biome:  # Day 2: we have a generator.
    def __init__(self, biome_type: Biomes = Biomes.OCEAN):  # Coordinates is a thing.
        self.name = biome_type.name
        self.structures = []  # Arrays.
        self.ordered_structures = []
        self.discovered = False
        for i in range(5):  # i needs to go so much things, it's quite sad.
            cur_struct = []  # Structures are good, i think.
            for j in range(5):  # Whiles... love them.
                val = biome_structures.get(
                    biome_type.value, {}
                )  # Biomes types are great, it wouldn't be a great game if there was only ocean. : LIES -3665 : What do you call Raft @slave -TCP : A Boat simulator 2nd in charge officer. - slave : Why are you not wrong -TCP
                ran = random.choices(list(val.keys()), val.values())[
                    0
                ]  # I'm still wondering what I am doing here.
                cur_struct.append(ran)  # Well at least i dont "annoy" anyone.
                self.structures.append(ran)
            self.ordered_structures.append(cur_struct)


"""World Gen"""  # UwU

biome_rarity = {
    "OCEAN": 0,
    "JUNGLE": 10,  # Lovely jungle.
    "CLIFF": 5,  # cant write what i was gonna write.
    "LAKE": 2,  # ohno. owo
    "SAND": 9,
    "GRASS": 5,
}


class World:
    def __init__(
        self,
        size: tuple = (25, 25),
        rarity: dict = biome_rarity,
        passes: int = 4,  # Someone is hijacking my comments with OwOs.
    ):  # i love minecraft, or <redacted>.
        self.chunks = []  # Chunks of biomes, what flavour is it?
        for w in range(size[0]):  # SIZES, THE BIGGER, the more there is.
            cur_chunks = []  # Chunks of meat.
            for h in range(size[1]):  # No clue what is happening here.
                """
                try:
                    orar = ((h*w)/(size[0]) + (w*h)/(size[1])) + ((size[0])/(w*h) + (size[1])/(w*h))
                except:
                    orar = 100
                print(orar)
                """
                if (h > size[1] - (size[1] / 10) or h < (size[1] / 10)) or (
                    w > size[0] - (size[0] / 10) or w < (size[1] / 10)
                ):
                    rarity["OCEAN"] += 25 + ((size[1] / 10) * (size[0] / 10))
                    chosen = random.choices(list(Biomes), rarity.values())[0]
                    rarity["OCEAN"] -= 25 + ((size[1] / 10) * (size[0] / 10))
                else:
                    next_to = [self.chunks[w - 1][h].name, cur_chunks[h - 1].name]
                    rarity[next_to[0]] += 30
                    rarity[next_to[1]] += 30
                    chosen = random.choices(list(Biomes), rarity.values())[
                        0
                    ]  # Need help, OwOs, UwUs and hewoo are annoying after some time.
                    rarity[next_to[0]] -= 30
                    rarity[next_to[1]] -= 30
                cur_chunks.append(Biome(chosen))  # Biome, you are the chosen one!
            self.chunks.append(cur_chunks)  # Chunks of biomes, lovely.
        for _ in range(passes):
            currentPass = self.chunks
            for y in range(len(self.chunks)):
                for x in range(len(self.chunks[y])):
                    try:
                        up = self.chunks[y - 1][x]
                    except:
                        up = Biome(Biomes.OCEAN)
                    try:
                        left = self.chunks[y][x - 1]
                    except:
                        left = Biome(Biomes.OCEAN)
                    try:
                        down = self.chunks[y + 1][x]
                    except:
                        down = Biomes(Biomes.OCEAN)
                    try:
                        right = self.chunks[y][x + 1]
                    except:
                        right = Biome(Biomes.OCEAN)
                    try:
                        cent = self.chunks[y][x]
                    except:
                        cent = Biome(Biomes.OCEAN)

                    ns = [up, down, left, right, cent]
                    chosen = random.choice(ns)

                    if self.chunks[y][x].name == "OCEAN":
                        chosen = Biome(Biomes.OCEAN)
                    if "LAKE" == cent.name and "OCEAN" in [b.name for b in ns]:
                        chosen = Biome(Biomes.SAND)
                    currentPass[y][x] = chosen
            self.chunks = currentPass
        for y in range(len(self.chunks)):
            for x in range(len(self.chunks[y])):
                try:
                    up = self.chunks[y - 1][x]
                except:
                    continue
                try:
                    left = self.chunks[y][x - 1]
                except:
                    continue
                try:
                    down = self.chunks[y + 1][x]
                except:
                    continue
                try:
                    right = self.chunks[y][x + 1]
                except:
                    continue
                try:
                    cent = self.chunks[y][x]
                except:
                    continue

                ns = [up, down, left, right, cent]

                if "LAKE" == cent.name and "OCEAN" in [b.name for b in ns]:
                    self.chunks[y][x] = Biome(Biomes.SAND)

class MiniWorld:
    def __init__(
        self,
        size: tuple = (25, 25),
        rarity: dict = biome_rarity,
        biome_size: int = 3,
        *_
    ):
        assert min(size) < 2  # The size must be at least (2, 2)

        x_biome_coords = random.sample(list(range(size[0] - 2)), (size[0] - 2) / 3)
        y_biome_coords = random.sample(list(range(size[1] - 2)), (size[1] - 2) / 3)

        orig_chunks = (
            [[Biome()] * size]
            + [[Biome()] + [None] * (size[0] - 2) + [Biome()]] * (size[1] - 2)
            + [[Biome()] * size]
        )

        for x, y in zip(x_biome_coords, y_biome_coords):
            self.chunks[x + 1][y + 1] = None

        self.chunks = []
