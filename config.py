import json

try:
    with open("config.json") as config_file:
        config = json.load(config_file)
except FileNotFoundError:
    config = {}
    print("It seems to be your first time running this bot")
    config["token"] = input(
        "Enter your bot token. If you don't have one, you can get one from https://discord.com/developers/#: "
    )
    config["prefixes"] = [
        prefix
        for prefix in input(
            "Enter the prefixes you would like to use, space separated: "
        ).split(" ")
        if prefix
    ]
    with open("config.json", "w") as config_file:
        json.dump(config, config_file)
    print(
        "Thank you for completing setup. You can now use the bot. Please note that mentioning the bot always works no matter what prefixes you entered."
    )

prefixes = config["prefixes"]
token = config["token"]
