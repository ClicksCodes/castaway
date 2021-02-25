import enum
import random
import math
from PIL import Image, ImageDraw, ImageFont
import numpy as np


class Biomes(enum.Enum):
    OCEAN = 0
    JUNGLE = 1
    CLIFF = 2
    LAKE = 3
    SAND = 4
    GRASS = 5


class Biome:
    def __init__(self, t:Biomes, coords:tuple):
        self.name = t.name
        self.discovered = True if self.name == "OCEAN" else False
        self.coords = coords


class World:
    def __init__(
        self, 
        size: tuple = (25, 25),
        rarity=None,
        passes: int = None,
        seed: int = 0,
        online: bool = False
    ):
        if passes is None:
            self.passes = ((size[0] + size[1])/2)-1
        else:
            self.passes = passes
        self.map = [[[] for _ in range(size[1])] for _ in range(size[0])]
        self.nnmap = self.map
        self.seed = seed
        self.online = online
        if rarity is None:
            rarity = {
                "OCEAN": float(0),
                "JUNGLE": float(15),
                "CLIFF": float(5),
                "LAKE": float(3),
                "SAND": float(0),
                "GRASS": float(5)
            }
        random.seed(a=self.seed, version=2)
        for y in range(size[1]):
            for x in range(size[0]):
                if math.sqrt((x-(size[0]/2))**2 + (y-(size[1]/2))**2) > size[0]-((3/5)*min(size[0], size[1])):
                    n = Biome(t=Biomes.OCEAN, coords=(x, y))
                else: 
                    beach = math.sqrt((x-(size[0]/2))**2 + (y-(size[1]/2))**2)**1.15
                    if beach > min(size[0], size[1])/3 and random.randint(0, 100) < beach: n = Biome(t=Biomes.SAND, coords=(x, y))
                    else: 
                        chosen = random.choices(list(Biomes), [n for n in rarity.values()])[0]
                        n = Biome(t=chosen, coords=(x, y))
                self.map[y][x] = n
        for _ in range(round(self.passes)):
            for y in range(size[1]):
                for x in range(size[0]):
                    if (min(x, y) == 0) or (x == len(self.map[0])-1) or (y == len(self.map)-1): continue
                    else: 
                        ne = [self.map[y - 1][x], self.map[y + 1][x], self.map[y][x - 1], self.map[y][x + 1]]
                        if "OCEAN" in [n.name for n in ne] and self.map[y][x].name == "LAKE":
                            self.nnmap[y][x] = Biome(t=Biomes.SAND, coords=(x, y))
                            continue
                        ne.append(self.map[y][x])
                        n = random.choice(ne)
                    self.nnmap[y][x] = n

            self.map = self.nnmap

    def mapimg(self, ctx, bot):
        def hex_to_rgb(value):
            lv = len(value)
            return tuple(int(value[i : i + lv // 3], 16) for i in range(0, lv, lv // 3))
        curMap = []

        cols = {
            "OCEAN": hex_to_rgb("71AFE5"),
            "JUNGLE": hex_to_rgb("60B358"),
            "CLIFF": hex_to_rgb("545454"),
            "LAKE": hex_to_rgb("78ECF2"),
            "SAND": hex_to_rgb("E6DC71"),
            "GRASS": hex_to_rgb("A1CC65"),
            "UNKNOWN": hex_to_rgb("000000"),
        }

        for chunkRow in self.map:
            cur_row = []
            for chunk in chunkRow:
                cur_row.append(cols[chunk.name])
                # if chunk.discovered == True:
                #     cur_row.append(cols[chunk.name])
                # else:
                #     cur_row.append(colors["UNKNOWN"])
            curMap.append(cur_row)

        im = Image.fromarray(np.uint8(curMap), mode="RGB")
        im = im.resize((1000, 1000), 0)  # 0 4
        font = ImageFont.truetype("fonts/roboto/Roboto-Bold.ttf", 24)
        draw = ImageDraw.Draw(im)
        x = bot.games[ctx.guild.id]['settings']
        draw.text((50, 960),f"{x['name']} | {ctx.guild.name} | Seed: {x['seed']}",hex_to_rgb("000000"),font=font)
        return im