import discord


class C:
    c = '\033[0m'

    RedDark = '\033[31m'
    GreenDark = '\033[32m'
    YellowDark = '\033[33m'
    BlueDark = '\033[34m'
    PinkDark = '\033[35m'
    CyanDark = '\033[36m'

    Red = '\033[91m'
    Green = '\033[92m'
    Yellow = '\033[93m'
    Blue = '\033[94m'
    Pink = '\033[95m'
    Cyan = '\033[96m'


colours = {
    "r": 0xF27878,
    "o": 0xE5AB71,
    "g": 0xA1CC65,
    "C": 0x78ECF2,
    "b": 0x71AFE5,
    "m": 0x8D58B2
}

emojis = {
    "xpStart":      "<:XPStart:757244282183745667>",
    "xpEnd":        "<:XPEnd:757244281898401903>",
    "xpMiddle":     "<:XPBlue:757244281537822783>",
    "xpIncomplete": "<:XPBlack:757244281609126038>",
    "starFull":     "<:Star:757244281139232799>",
    "starEmpty":    "<:BlankStar:757244281219055639>",
    "Warning":      "<:Warning:791676335675277382>",
    "Cooking":      "<:Cooking:791676335356772392>",
    "Exploring":    "<:Exploring:791676335512092672>",
    "Crafting":     "<:Crafting:791676335428075590>",
    "Scavenging":   "<:Scavenging:791676335733866516>",
    "Fishing":      "<:Fishing:791676335708700682>",
    "RankCard":     "<:RankCard:791676335751561216>",
    "right":        "<:right:791683268902649876>",
    "left":         "<:left:791683268876697610>",
    "cross":        "<:cross:791683553741111336>",
    "tick":         "<:tick:791683415131815946>",
    "Name":         "<:Name:794172731356348417>",
    "Max_Players":  "<:Max_Players:794172731381252096>",
    "Size":         "<:Size:794172731708932116>",
    "Seed":         "<:Seed:794172731439579188>",
    "Difficulty": {
        1: "<:Difficulty1:794172730827997185>",
        2: "<:Difficulty2:794172731032993793>",
        3: "<:Difficulty3:794172731125530665>"
    },
    "Online": {
        0: "<:Online2:794172731263287297>",
        1: "<:Online1:794172731473002536>"
    }
}

lembed = discord.Embed(title="Loading", color=colours["g"])
