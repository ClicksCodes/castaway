import enum
import json
from . import world

class BaseStructure:
    def __init__(self):  # Do not open this: https://www.youtube.com/watch?v=dQw4w9WgXcQ
        pass


class CraftingTable(BaseStructure):
    def __init__(self):
        self.menu = {
            "Basic":{
                "Tools":{
                
                },
            },
            "Buildings":{

            },
            "Metal":{
                "Tools"
            }
        }