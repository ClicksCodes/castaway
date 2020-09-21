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


class Resource:  # So enums if "set of options"?
    def __init__(self):  # i have no clue what it is for.
        pass  # It is quite depressing.. 

    pass  # I'll PASS on that.


class BasicResource(Resource):  # Is nothing something?
    pass # I'll PASS on that. (the same shit joke in a row, what a pitty).


class ProcessedResource(  # I was asked to comments each and every line of codes.
    Resource  # So yep, im commenting all the lines with code in it.
):  # I swear Minion never seen that video: https://www.youtube.com/watch?v=y566MWHAV3Y
    pass  # Serious stuff here: if you feel depressed, call childline: 0800 1111 (uk only if i am correct)


class Wood(  # 
    BasicResource
):  # We are the world, we are the people, we are the one making a better place so let's start giving. Great music.
    pass


class Rock(BasicResource):  # He used to be a lonely guy, not anymore.
    pass


class Sand(
    BasicResource
):  # Minion is not as good as you might think; he uses light theme EVERYWHERE and no one likes it. Yikes. : I like it so shut
    pass  # light theme best


class Ore(BasicResource):
    pass


class Metal(ProcessedResource):
    pass  # Most trees are not always the same size -TCP


"""Collectables"""


class Collectable:
    def __init__(self):  # isnt this script a bit too long? like it really feels like YandereDev code but looks nicer and all but
        pass    # Extremely long, wouldnt it impact on performance?

    pass


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

    def drops(self, member):
        # I only know simple python, so i dont know what the flip is happening here.
        x = random.randint(-1, 1)
        damt = (
            round(
                self.drops_amounts[self.size]
                * (1 + skills.get(member, skills.Skills.EXPLORING) * random.random())  # In reality, I am a slave and a test player... or not.
            )
            + x
        )  # random.random gives you a number between 0-1, first useful message there.
        return self.drops, damt  # Pokemon is a great franchise.


class AdvancedNaturalStructure(NaturalStructure):
    def __init__(self, size, resources):  # If this is going to be PayToWin, im taking 50% of the 
        pass


class Tree(NaturalStructure):
    # So serious stuff here, these are trees. But what type? Oak? Jungle? Acasia? Birch?
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
        self, size=Size.SMALL, drops=Ore()
    ):  # Arstotzka loves ores, ores are now Arstotzka's second favorite object.
        super().__init__(size, drops)


class Beach(AdvancedNaturalStructure):  # oh structures?
    resources = [Sand, Treasure]  # Treasures in sand -- originality.


class Cave(AdvancedNaturalStructure):  # Caves, lots of them.
    resources = [Rock, OreVein]  # Veins are everywhere, deep inside the earth to inside your body -- blood veins.

    def __init__(self, thing):  # stuff working by itself?
        pass  # Pass it on.


# drops = [Tree(Size.SMALL), Tree(Size.MEDIUM), Tree(Size.LARGE)]  # Trees makes great paper. : Arstotzka likes paper. Paper please says Arstotzka -3665


"""Biomes"""  # Ive lost hope in hooman being.


class Biomes(enum.Enum):  # I am writing this down to up so things might get weird, sentence wise.
    OCEAN = 0  # Anything after this is going or is already unreadable as it doesnt make sense: 
    JUNGLE = 1  # Never been into a jungle but, after reading the jungle book, it doesnt really change any opinions on if you would go into a jungle.
    CLIFF = 2  # Cliffs are also nice, you can see a lot.
    LAKE = 3  # On the other hand, lakes. Best thing ever. you dont get dirty, +10 if it as pebbles.
    SAND = 4  # Sand is just annoying, like you go to the beach, you go into the water and, YOU HAVE SAND EVERYWHERE!
    GRASS = 5  # Anyone used to put grass in their cereals? i used to for some dark and unknown reasons.


biome_structures = {  # These are not worth commenting
    0: {  # Just look at them,
        Beach: 3,  # I really have no idea what to write here.
    },  # Useless, only holding code together,
    1: {  # Doing nothing else,
        Tree: 50,  # I mean, there is plenty of space and all,
        Cave: 2,  # But you know, there isnt much we can write,
        OreVein: 4,  # We could talk about the oreVeins,
    },  # just holdin'
    2: {  # and holdin'
        Tree: 10,  # Or the trees and how they'll gonna work,
        Cave: 2,  # But that is just plain boring,
        OreVein: 5,  # Actually, why is oreVeins twice here?
    },  # Still doing the same job
    3: {  # and here too!
        Beach: 2,  # And beach?
    },  # Guess what? here too.
    4: {  # aaaand here.
        Tree: 5,  # And trees?
        OreVein: 5,  # Must be normal, or is it?
    },  # Minion love them.
    5: {  # here too.
        Tree: 15,  # AND SOME MORE TREES HERE!!
        OreVein: 4,  # I really dont understand why,
        Cave: 2,  # Maybe if i were to read the code...
    },  # im not even bothered putting caps anymore.
}  # like i am not paid for this, and for the best. : What if you were @slave? -TCP : That would be fantastic - slave : How much would you like? -TCP : 3 quid an hour is good enough really. - slave : It shall be done -TCP : Here is my paypal.me: https://paypal.me/thefroggie85/
# hour 1 @slave, start working -TCP : ok 2nd in charge officer.

class BiomeGen:  # Day 2: we have a generator.
    def __init__(self, biome_type: Biomes = Biomes.OCEAN):  # Coordinates is a thing.
        structures = []  # Arrays.

        i = 0  # And i too.
        while i < 5:  # i needs to go so much things, it's quite sad.
            cur_struct = []  # Structures are good, i think.
            x = 0  # X is always 0... that sound like bullying to me.
            while x < 5:  # Whiles... love them.
                val = Structures(biome_type)  # Biomes types are great, it wouldn't be a great game if there was only ocean. : LIES -3665 : What do you call Raft @slave -TCP : A Boat simulator 2nd in charge officer. - slave : Why are you not wrong -TCP
                i = random.randint(0, 1)  # RANDOMS!
                if i == 0: ran = None  # Fact: Death Stranding is just a walking simulator for the enormous price of 60 quid. + Extra monster sponsoring.
                else: ran = random.choices(val.keys(), val.values(), k=1)  # I'm still wondering what I am doing here.
                cur_struct.append(ran)  # Well at least i dont "annoy" anyone.
                x += 1
            structures.append(cur_struct)
            i += 1


"""World Gen"""  # UwU

biome_rarity = {
    "ocean": 0,
    "jungle": 10,  # Lovely jungle.
    "cliff": 5,  # cant write what i was gonna write.
    "lake": 5,  # ohno. owo
    "sand": 7,
    "grass": 7
}

class World:
    def __init__(
        self, size: tuple, rarity: dict = biome_rarity  # Someone is hijacking my comments with OwOs.
    ):  # i love minecraft, or <redacted>.
        chunks = []  # Chunks of biomes, what flavour is it?
        for w in range(size[0]):  # SIZES, THE BIGGER, the more there is.
            cur_chunks = []  # Chunks of meat.
            for h in range(size[1]):  # No clue what is happening here.
                chosen = random.choices(Biomes, rarity, k=1)  # Need help, OwOs, UwUs and hewoo are annoying after some time.
                cur_chunks.append(BiomeGen(Biomes(chosen)))  # Biome, you are the chosen one!
                print(cur_chunks[h])
            chunks.append(cur_chunks)  # Chunks of biomes, lovely.

world = World(size=(5, 5))
print(world.chunks)