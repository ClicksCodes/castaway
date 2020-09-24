import json
from . import craftables
from . import smeltables
from . import islanders
from . import world
import discord

def flatten(obj):
    flattened = []

    for k, v in obj.items():
        if isinstance(v, dict):
            for item in flatten(v):
                flattened.append(item)
        else:
            for item in v:
                flattened.append(item)

    return flattened

def find(obj, thing):

    path = []


    for key, value in obj.items():
        if isinstance(value, list) and thing in value:
            path.append(key)
        elif isinstance(value, dict) and (p := find(value, thing)):
            path += p
        elif thing == getattr(value, "name", None):
            path.append(thing)
    print(path)
    return path


class Inventory:

    menu = {
        "tools":[
            craftables.WoodAxe,
            craftables.WoodHoe,
            craftables.WoodPickaxe,
            craftables.WoodShovel,
            craftables.WoodScythe
        ],
        "buildings":[
            craftables.Workbench,
            craftables.Firepit
        ],
        "resources": [
            craftables.BundledLogs
        ]
    }

    @classmethod
    def canMake(cls, ctx):

        user_inv = [["wood", 15],["stick", 10],["plantfiber", 20]]#islanders.get_data_for(ctx.author)["inventory"]["items"]

        craftable = cls.menu.copy()
        
        for craft_type in craftable:
            for item in craft_type:
                for key, value in item.recipe.items():
                    if inv_items.get(key.name, 0) < int(value):
                        del craft_type[key]
        print(craftable)
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

    @classmethod
    def canMake(cls, ctx):
        user_inv = islanders.get_data_for(ctx.author)["inventory"]["items"]

        flattened = flatten(cls.menu)

        inv_items = {}
        
        for item, amount in user_inv:
            inv_items[item] = inv_items.get(item, 0) + amount

        craftable = []

        for item in flattened:
            for key, value in item.recipe.items():
                print(inv_items.get(key.name, 0))
                if inv_items.get(key.name, 0) < int(value):
                    break
            else:
                craftable.append(item)

        return craftable


class Smelting:
    menu = {
        "ores": [smeltables.Copper,smeltables.Bronze,smeltables.Iron],
        "other": [smeltables.Glass]
    }

    @classmethod
    def canMake(cls, ctx):
        user_inv = islanders.get_data_for(ctx.author)["inventory"]["items"]

        flattened = flatten(cls.menu)

        inv_items = {}
        
        for item, amount in user_inv:
            inv_items[item] = inv_items.get(item, 0) + amount

        craftable = []

        for item in flattened:
            for key, value in item.recipe.items():
                print(inv_items.get(key.name, 0))
                if inv_items.get(key.name, 0) < int(value):
                    break
            else:
                craftable.append(item)

        return craftable

class ToolSmith:
    menu = {
        "wood": [craftables.WoodAxe, craftables.WoodHoe, craftables.WoodPickaxe, craftables.WoodShovel, craftables.WoodScythe],
        "copper": [craftables.CopperAxe,craftables.CopperHoe,craftables.CopperPickaxe,craftables.CopperShovel,craftables.CopperScythe],
        "iron": [craftables.IronAxe, craftables.IronHoe, craftables.IronPickaxe, craftables.IronShovel, craftables.IronScythe]
    }

    @classmethod
    def canMake(cls, ctx):
        user_inv = islanders.get_data_for(ctx.author)["inventory"]["items"]

        flattened = flatten(cls.menu)

        inv_items = {}
        
        for item, amount in user_inv:
            inv_items[item] = inv_items.get(item, 0) + amount


        craftable = []

        for item in flattened:
            for key, value in item.recipe.items():
                print(inv_items.get(key.name, 0))
                if inv_items.get(key.name, 0) < int(value):
                    break
            else:
                craftable.append(item)

        return craftable

async def sendEmbed(ctx, cr_type):
    if cr_type == "inv":
        d = Inventory.canMake(ctx=ctx)
    elif cr_type == "craft":
        d = Crafting.canMake(ctx=ctx)
    elif cr_type == "smelt":
        d = Smelting.canMake(ctx=ctx)
    elif cr_type == "tool":
        d = ToolSmith.canMake(ctx=ctx)
    else:
        raise TypeError

    e = discord.Embed(title="Yes")


    await ctx.send(f"{items}")