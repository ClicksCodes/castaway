from cogs.castaway import world
from PIL import Image, ImageDraw
import numpy as np

dimensions = (1000, 1000)
mapsize = (10, 10)


def hex_to_rgb(value):
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

colors = {
    "OCEAN":  hex_to_rgb("71AFE5"),
    "JUNGLE": hex_to_rgb("60B358"),
    "CLIFF":  hex_to_rgb("545454"),
    "LAKE":   hex_to_rgb("78ECF2"),
    "SAND":   hex_to_rgb("E6DC71"),
    "GRASS":  hex_to_rgb("A1CC65")
}

game = world.World(mapsize)

for chunkRow in game.chunks:
    for chunk in chunkRow:
        for structRow in chunk.structures:
            for struct in structRow:
                try: stype = struct.__name__
                except: stype = None
                print(f"{stype} in chunk {chunk.biome.name}")

curMap = []

for chunkRow in game.chunks:
    curRow = []
    for chunk in chunkRow:
        curRow.append(colors[chunk.biome.name])
    curMap.append(curRow)
print(curMap)

im = Image.fromarray(np.uint8(curMap),mode='RGB')
print(im)
im = im.resize(dimensions, 4) # 0 4
im.show()
