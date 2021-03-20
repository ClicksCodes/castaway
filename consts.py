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
    "xpStart":      757244282183745667,
    "xpEnd":        757244281898401903,
    "xpMiddle":     757244281537822783,
    "xpIncomplete": 757244281609126038,
    "starFull":     757244281139232799,
    "starEmpty":    757244281219055639,
    "Warning":      791676335675277382,

    "Transfer":     822773231261712386,
    "Delete":       822773231307849768,
    "Sort":         822781647379234846,

    "Cooking":      791676335356772392,
    "Exploring":    791676335512092672,
    "Crafting":     791676335428075590,
    "Scavenging":   791676335733866516,
    "Fishing":      791676335708700682,
    "Sailing":      822147260384149535,
    "Mining":       822147260770025553,
    "Farming":      822147260451258369,

    "RankCard":     791676335751561216,
    "right":        791683268902649876,
    "left":         791683268876697610,
    "cross":        791683553741111336,
    "tick":         791683415131815946,
    "Name":         794172731356348417,
    "Max_Players":  794172731381252096,
    "Size":         794172731708932116,
    "Seed":         794172731439579188,
    "Difficulty": {
        1: 794172730827997185,
        2: 794172731032993793,
        3: 794172731125530665
    },
    "Online": {
        0: 794172731263287297,
        1: 794172731473002536
    }
}

lembed = discord.Embed(title="Loading", color=colours["g"])
