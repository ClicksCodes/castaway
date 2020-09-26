import json
from . import craftables
from . import smeltables
from . import islanders
from . import world
import discord, copy

class CanCraft:
    @classmethod
    def canMake(cls, ctx, suffix=False):

        user_inv = islanders.get_data_for(ctx.author)["inventory"]["items"]


        inv_items = {}
        for item, amount in user_inv:
            inv_items[item] = inv_items.get(item, 0) + amount

        craftable = copy.deepcopy(cls.menu)
        for _, craftables in craftable.items():
            print(craftables)
            for item in craftables.copy():
                for key, value in item.recipe.items():
                    if inv_items.get(key.name, 0) < value:
                        craftables.remove(item)

                        break

        return {k + f" (at {cls.location})": v for k, v in craftable.items()} if suffix else craftable

    @classmethod
    def canMakeAll(cls, ctx, suffix=False):

        user_inv = islanders.get_data_for(ctx.author)["inventory"]["items"]

        inv_items = {}
        for item, amount in user_inv:
            inv_items[item] = inv_items.get(item, 0) + amount

        return {k + f" (at {cls.location})": v for k, v in cls.menu.items()} if suffix else cls.menu


class Inventory(CanCraft):
    location = "all times"
    menu = {
        "tools": [
            craftables.WoodAxe,
            craftables.WoodHoe,
            craftables.WoodPickaxe,
            craftables.WoodShovel,
            craftables.WoodScythe,
        ],
        "buildings": [craftables.Workbench, craftables.Firepit],
        "resources": [craftables.BundledLogs],
    }

    @classmethod
    def sendCraftables(cls, ctx, cr_type):
        if cr_type == "inv":
            d = cls.canMake(ctx=ctx)
        elif cr_type == "craft":
            d = Crafting.canMake(ctx=ctx)
        elif cr_type == "smelt":
            d = Smelting.canMake(ctx=ctx)
        elif cr_type == "tool":
            d = ToolSmith.canMake(ctx=ctx)
        else:
            d = dict(
                cls.canMake(ctx=ctx, suffix=True), 
                **Crafting.canMake(ctx=ctx, suffix=True), 
                **Smelting.canMake(ctx=ctx, suffix=True), 
                **ToolSmith.canMake(ctx=ctx, suffix=True)
            )

        x = 0

        e = discord.Embed(
            title="Craftables:",
            color=0x71AFE5
        )


        for key, values in d.items():
            if not len(values):
                continue
            desc = ""
            for value in values:
                x += 1
                rec = ", ".join([f"{v}x{k.name.capitalize()}" for k, v in value.recipe.items()])
                desc += f"[{x}] {value.name.capitalize()} - {rec}\n"
            e.add_field(name=key.upper(), value=desc)

        e.description = "*You can't craft anything, collect some items first*" if not len(e.fields) else ""

        return (e, flatten(d))

    @classmethod
    def sendAllCraftables(cls, ctx, cr_type):
        if cr_type == "inv":
            d = cls.canMakeAll(ctx=ctx)
        elif cr_type == "craft":
            d = Crafting.canMakeAll(ctx=ctx)
        elif cr_type == "smelt":
            d = Smelting.canMakeAll(ctx=ctx)
        elif cr_type == "tool":
            d = ToolSmith.canMakeAll(ctx=ctx)
        else:
            d = dict(
                cls.canMakeAll(ctx=ctx, suffix=True), 
                **Crafting.canMakeAll(ctx=ctx, suffix=True), 
                **Smelting.canMakeAll(ctx=ctx, suffix=True), 
                **ToolSmith.canMakeAll(ctx=ctx, suffix=True)
            )

        desc = ""
        x = 0
        
        e = discord.Embed(
            title="All Craftables:",
            color=0x71AFE5
        )


        for key, values in d.items():
            if not len(values):
                continue
            desc = ""
            for value in values:
                x += 1
                rec = ", ".join([f"{v}x{k.name.capitalize()}" for k, v in value.recipe.items()])
                desc += f"[{x}] {value.name.capitalize()} - {rec}\n"
            e.add_field(name=key.upper(), value=desc)

        return (e, flatten(d))

    @staticmethod
    async def send(ctx):
        e = discord.Embed(
            title="Inventory:",
            description="\n".join(
                f"{item}: {amount}" for item, amount in islanders.get_data_for(ctx.author)["inventory"]["items"]
            ) or "*No items*",
            color=0x71AFE5,
        )
        return await ctx.send(
            embed=e
        )


class Crafting(CanCraft):
    location = "a workbench"
    menu = {
        "tools": [
            craftables.WoodAxe,
            craftables.WoodHoe,
            craftables.WoodPickaxe,
            craftables.WoodShovel,
            craftables.WoodScythe,
            craftables.CopperAxe,
            craftables.CopperHoe,
            craftables.CopperPickaxe,
            craftables.CopperShovel,
            craftables.CopperScythe,
        ],
        "resources": [craftables.BundledLogs, craftables.String, craftables.Rope],
        "buildings": [
            craftables.Workbench,
            craftables.OreOven,
            #craftables.ToolBench,
            craftables.Hut,
            craftables.Storage,
            craftables.LargeStorage,
            craftables.Firepit,
            craftables.UpgradedHut,
        ],
        "endgame": [craftables.Sail, craftables.Boat],
    }
    

class Smelting(CanCraft):
    location = "an ore oven"
    menu = {
        "ores": [smeltables.Copper, smeltables.Bronze, smeltables.Iron],
        "other": [smeltables.Glass],
    }


class ToolSmith(CanCraft):
    location = "a tool bench"
    menu = {
        "wood": [
            craftables.WoodAxe,
            craftables.WoodHoe,
            craftables.WoodPickaxe,
            craftables.WoodShovel,
            craftables.WoodScythe,
        ],
        "copper": [
            craftables.CopperAxe,
            craftables.CopperHoe,
            craftables.CopperPickaxe,
            craftables.CopperShovel,
            craftables.CopperScythe,
        ],
        "iron": [
            craftables.IronAxe,
            craftables.IronHoe,
            craftables.IronPickaxe,
            craftables.IronShovel,
            craftables.IronScythe,
        ],
    }



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
