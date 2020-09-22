import random
import json
import enum

class Skills(enum.Enum):
    COOKING = 0  # <one redacted message later> - pinea : *If you can guess what that redacted once said, please get in contact because you're as bad as us -3665*
    EXPLORING = 1  # Since when can you explore VCs? : D D D D D D DORA THE EXPLORER.
    CRAFTING = 2  # Sounds like minecraft.
    BUILDING = 3  # Bob the Builder be like.
    SCAVENGING = 4  # Slave's work.
    FISHING = 5  # Sponge bob remembered that.


def get_data_for(member):
    with open(f"data/{member.guild.id}.json") as data_file:
        data = json.load(data_file)

    data["islanders"][str(member.id)] = data["islanders"].get(
        str(member.id),
        {
            "skills": {random.choice(list(Skills)): 3},
            "action": None,
            "inventory": {"slots": 8, "stack_size": 32, "items": []},
        },
    )
    return data["islanders"][str(member.id)]

def write_data_for(member, data):
    with open(f"data/{member.guild.id}.json") as data_file:
        json.dump(data, data_file)

def inventory_add(previous, item, amount):
            # "inventory": {
            #     "slots": 8,
            #     "stack_size": "32",
            #     "items": [
            #         ["computer", 5],
            #         ["knowledge", 0],
            #         ["believed_knowledge", 1000],
            #         ["will_to_live", 0]
            #     ]
            # }
    stack_size = previous["stack_size"]
    for slot, item in enumerate(previous["items"]):
        if item[0] == item:
            amount_to_transfer = min(stack_size - item[1], amount)
            previous["items"][slot][1] = item[1] + amount_to_transfer
            amount = amount - amount_to_transfer
        if amount <= 0:
            break
    else:
        while amount > 0 and len(previous["items"]) < previous["slots"]:
            amount_to_transfer = min(stack_size, amount)
            previous["items"].append((item, amount_to_transfer))
            amount -= amount_to_transfer
    return previous
