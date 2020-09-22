import enum
import json
from . import craftables
from . import smeltables
from . import islanders
from discord.ext import menus
from . import world


class Inventory(menus.Menu):
    """
    async def send_initial_message(self, ctx):

        self.user_inv = islanders.get_data_for(ctx.author)["inventory"]["items"]

        backn = '\n'

        embed = discord.Embed(
            title=f"{ctx.author.name}'s inventory"
            description=f"{[
                f'{item} : {amount}{backn}' for item, amount in user_inv 
            ]}"
            color=0x71AFE5
        )
        return await ctx.send(embed=embed)
    """
    #@menus.button()
    def craft(self, ctx):

        self.user_inv = [[world.Wood, 20],[world.Stick, 20]]#islanders.get_data_for(ctx.author)["inventory"]["items"]

        possible = [craftables.WoodAxe, craftables.WoodHoe, craftables.WoodPickaxe,craftables.WoodShovel, craftables.WoodScythe, craftables.Workbench, craftables.BundledLogs, craftables.Firepit]

        inv_items = [item[0] for item in self.user_inv]
        craftable = []

        for item in possible:
            print(item)
            for key, value in item.recipe:
                print(key, value)
                if key in inv_items and inv_items[key][1] > int(value):
                    craftable += key
                    print("added to craftable")

class Crafting:
    def __init__(self):
        self.menu = {
            "Basic":{
                "Tools":[
                    craftables.WoodAxe.recipe
                ],
                "Buildings":[

                ]
            },
            "Stone":{

            },
            "Metal":{
                "Tools"
            }
        }