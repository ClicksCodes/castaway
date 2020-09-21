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
            "skills": {
                random.choice(list(Skills)): 3
            },
            "action": None,
            "inventory": {
                "slots": 8,
                "stack_size": 32,
                "items": {
                }
            }
        }
    )