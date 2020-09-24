import json
from . import craftables
from . import smeltables
from . import islanders
from . import world
import discord


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

        user_inv = islanders.get_data_for(ctx.author)["inventory"]["items"] #[["wood", 15],["stick", 10],["plantfiber", 20]]#

        inv_items = {}
        for item, amount in user_inv:
            inv_items[item] = inv_items.get(item, 0) + amount

        craftable = cls.menu.copy()
        for _, craftables in craftable.items():
            for item in craftables:
                for key, value in item.recipe.items():
                    if inv_items.get(key.name, 0) < int(value):
                        craftables.remove(item)
                        break
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

        inv_items = {}
        
        for item, amount in user_inv:
            inv_items[item] = inv_items.get(item, 0) + amount

        craftable = cls.menu.copy()
        for _, craftables in craftable.items():
            for item in craftables:
                for key, value in item.recipe.items():
                    if inv_items.get(key.name, 0) < int(value):
                        craftables.remove(item)
                        break
        return craftable


class Smelting:
    menu = {
        "ores": [smeltables.Copper,smeltables.Bronze,smeltables.Iron],
        "other": [smeltables.Glass]
    }

    @classmethod
    def canMake(cls, ctx):
        user_inv = islanders.get_data_for(ctx.author)["inventory"]["items"]

        inv_items = {}
        
        for item, amount in user_inv:
            inv_items[item] = inv_items.get(item, 0) + amount

        craftable = cls.menu.copy()
        for _, craftables in craftable.items():
            for item in craftables:
                for key, value in item.recipe.items():
                    if inv_items.get(key.name, 0) < int(value):
                        craftables.remove(item)
                        break
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

        inv_items = {}
        
        for item, amount in user_inv:
            inv_items[item] = inv_items.get(item, 0) + amount

        craftable = cls.menu.copy()
        for _, craftables in craftable.items():
            for item in craftables:
                for key, value in item.recipe.items():
                    if inv_items.get(key.name, 0) < int(value):
                        craftables.remove(item)
                        break
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

    e = discord.Embed(
        title="Craftables:",
        description="\n\n".join([(f"__**{key.upper()}**__:\n" + "\n".join([value.name.capitalize() for value in values])) for key, values in d.items()]),
        color=0x71afe5
    )


    return await ctx.send(embed=e)