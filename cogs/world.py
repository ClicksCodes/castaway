import enum
import random
import math
import functools
import asyncio
import discord
import datetime
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
    def __init__(self, t: Biomes, coords: tuple):
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
        online: bool = False,
        name: str = "Castaway Island",
        bot: any = None
    ):
        if passes is None:
            self.passes = ((size[0] + size[1])/2)-1
        else:
            self.passes = passes
        self.map = [[[] for _ in range(size[1])] for _ in range(size[0])]
        self.nnmap = self.map
        self.seed = seed
        self.online = online
        self.name = name
        self.bot = bot
        self.size = size
        self.rarity = rarity

        result = self.bot.loop.run_in_executor(None, self.genmap)

    def genmap(self):
        if self.rarity is None:
            self.rarity = {
                "OCEAN": float(0),
                "JUNGLE": float(15),
                "CLIFF": float(5),
                "LAKE": float(3),
                "SAND": float(0),
                "GRASS": float(5)
            }
        random.seed(a=self.seed, version=2)

        for y in range(self.size[1]):
            for x in range(self.size[0]):
                if math.sqrt((x-(self.size[0]/2))**2 + (y-(self.size[1]/2))**2) > self.size[0]-((3/5)*min(self.size[0], self.size[1])):
                    n = Biome(t=Biomes.OCEAN, coords=(x, y))
                else:
                    beach = abs(math.sqrt((x-(self.size[0]/2))**2 + (y-(self.size[1]/2))**2)**1.15)
                    beach2 = beach / min(self.size[0], self.size[1])
                    beach2 *= 150
                    if beach > min(self.size[0], self.size[1])/3 and random.randint(0, 100) < beach2:
                        n = Biome(t=Biomes.SAND, coords=(x, y))
                    else:
                        chosen = random.choices(list(Biomes), [n for n in self.rarity.values()])[0]
                        n = Biome(t=chosen, coords=(x, y))
                self.map[y][x] = n
        for _ in range(round(self.passes)):
            for y in range(self.size[1]):
                for x in range(self.size[0]):
                    if (min(x, y) == 0) or (x == len(self.map[0])-1) or (y == len(self.map)-1):
                        continue
                    else:
                        ne = [self.map[y - 1][x], self.map[y + 1][x], self.map[y][x - 1], self.map[y][x + 1]]
                        if "OCEAN" in [n.name for n in ne] and self.map[y][x].name == "LAKE":
                            self.nnmap[y][x] = Biome(t=Biomes.SAND, coords=(x, y))
                            continue
                        ne.append(self.map[y][x])
                        n = random.choice(ne)
                    self.nnmap[y][x] = n

            self.map = self.nnmap

    async def mapimg(self, ctx):
        for _ in range(30):
            if self.map[-1][-1] == []:
                await asyncio.sleep(1)
            else:
                break
        if self.map[-1][-1] == []:
            return 408

        def hex_to_rgb(value):
            lv = len(value)
            return tuple(int(value[i: i + lv // 3], 16) for i in range(0, lv, lv // 3))

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
            curMap.append(cur_row)

        im = Image.fromarray(np.uint8(curMap), mode="RGB")
        size = 1000
        while size % self.size[0] != 0:
            size -= 1
        im = im.resize((1000, 1000), 0)  # 0 4
        font = ImageFont.truetype("fonts/roboto/Roboto-Bold.ttf", 24)
        draw = ImageDraw.Draw(im)
        draw.text((50, 960), f"{self.name} | {ctx.guild.name} | Seed: {self.seed}", hex_to_rgb("000000"), font=font)
        return im
