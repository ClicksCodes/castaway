import random
import datetime
from consts import *


class Player:
    def __init__(self, i):
        self.id = i
        self.joined = datetime.datetime.utcnow()
        self.skills = {
            "Cooking":    [0, emojis["Cooking"]],
            "Exploring":  [0, emojis["Exploring"]],
            "Crafting":   [0, emojis["Crafting"]],
            "Scavenging": [0, emojis["Scavenging"]],
            "Fishing":    [0, emojis["Fishing"]]
        }
        self.level = 1
        self.upgradesUsed = 0
        self.xp = 0
        self.skills[random.choice(list(self.skills.keys()))][0] = 2

        self.task = {
            "active": False,
            "type": None,
            "started": None
        }
