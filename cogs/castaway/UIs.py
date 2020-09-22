import enum
import json
from . import craftables
from . import smeltables
from . import islanders
from . import world


class Inventory:
    @staticmethod
    async def send(ctx):

        user_inv = islanders.get_data_for(ctx.author)["inventory"]["items"]

        backn = '\n'

        embed = discord.Embed(
            title=f"{ctx.author.name}'s inventory",
            description=f"{[f'{item} : {amount}{backn}' for item, amount in user_inv]}",
            color=0x71AFE5
        )
        return await ctx.send(embed=embed)
    
    
    @staticmethod
    async def craft(ctx):

        user_inv = islanders.get_data_for(ctx.author)["inventory"]["items"]

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

        inv_items = {}

        for item, amount in user_inv:
            inv_items[item] = inv_items.get(item, 0) + amount 

        craftable = []

        for item in possible:
            for key, value in item.recipe.items():
                if inv_items.get(key.name, 0) < int(value):
                    break
            else:
                craftable.append(item)
        


class Crafting:
    def __init__(self):
        self.menu = {
            "Basic": {"Tools": [craftables.WoodAxe.recipe], "Buildings": []},
            "Stone": {},
            "Metal": {"Tools"},
        }
