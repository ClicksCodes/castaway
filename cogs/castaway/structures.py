import enum
import json
from . import craftables
from . import smeltables

class BaseStructure:
    def __init__(self):  # Do not open this: https://www.youtube.com/watch?v=dQw4w9WgXcQ
        pass


class Workbench(BaseStructure):
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