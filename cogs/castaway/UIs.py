import enum
import json
from . import craftables
from . import smeltables
from . import islanders
from . import world
import discord

class Inventory:

    possible = [
            craftables.WoodAxe,
            craftables.WoodHoe,
            craftables.WoodPickaxe,
            craftables.WoodShovel,
            craftables.WoodScythe,
            craftables.Workbench,
            craftables.BundledLogs,
            craftables.Firepit,
    ]

    def canMake(self, ctx):

        user_inv = islanders.get_data_for(ctx.author)["inventory"]["items"]

        inv_items = {}

        for item, amount in user_inv:
            inv_items[item] = inv_items.get(item, 0) + amount

        craftable = []

        for item in self.possible:
            for key, value in item.recipe.items():
                if inv_items.get(key.name, 0) < int(value):
                    break
            else:
                craftable.append(item)

        return craftable


class Crafting:
    menu = {
        "tools": {
            "wood":[craftables.WoodAxe, craftables.WoodHoe, craftables.WoodPickaxe, craftables.WoodShovel, craftables.WoodScythe],
            "copper":[craftables.CopperAxe,craftables.CopperHoe,craftables.CopperPickaxe,craftables.CopperShovel,craftables.CopperScythe]
        },
        "resources": [craftables.BundledLogs, craftables.String, craftables.Rope],
        "buildings": [craftables.Workbench, craftables.OreOven, craftables.ToolBench, craftables.Hut, craftables.Storage, craftables.LargeStorage, craftables.Firepit, craftables.UpgradedHut],
        "endgame": [craftables.Sail,craftables.Boat]
    }

    def canMake(self, ctx):
        user_inv = islanders.get_data_for(ctx.author)["inventory"]["items"]

        flatten = [k,v for k,v in self.menu.items()]



class Smelting:
    def __init__(self):
        menu = {
            "ores": [smeltables.Copper,smeltables.Bronze,smeltables.Iron],
            "other": [smeltables.Glass]
        }

class ToolSmith:
    def __init__(self):
        menu = {
            "wood": [craftables.WoodAxe, craftables.WoodHoe, craftables.WoodPickaxe, craftables.WoodShovel, craftables.WoodScythe],
            "copper": [craftables.CopperAxe,craftables.CopperHoe,craftables.CopperPickaxe,craftables.CopperShovel,craftables.CopperScythe],
            "iron": [craftables.IronAxe, craftables.IronHoe, craftables.IronPickaxe, craftables.IronShovel, craftables.IronScythe]
        }