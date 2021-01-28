from cogs import world
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import math
import time


def generateMap(mapsize=(35, 35), passes=None):
    mult = 1000 / (max((mapsize[0], mapsize[1])))

    dimensions = (mapsize[1] * int(mult), mapsize[0] * int(mult))

    def hex_to_rgb(value):
        lv = len(value)
        return tuple(int(value[i : i + lv // 3], 16) for i in range(0, lv, lv // 3))

    colors = {
        "OCEAN": hex_to_rgb("71AFE5"),
        "JUNGLE": hex_to_rgb("60B358"),
        "CLIFF": hex_to_rgb("545454"),
        "LAKE": hex_to_rgb("78ECF2"),
        "SAND": hex_to_rgb("E6DC71"),
        "GRASS": hex_to_rgb("A1CC65"),
        "UNKNOWN": hex_to_rgb("000000"),
    }

    if passes == None: passes = int((math.sqrt(min((mapsize[0], mapsize[1])))) - 1)
    game = world.World(mapsize, passes=passes, seed=69420)

    


generateMap()
