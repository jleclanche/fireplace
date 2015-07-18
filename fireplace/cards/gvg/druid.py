from ..utils import *


##
# Minions

# Attack Mode (Anodized Robo Cub)
class GVG_030a:
	play = Buff(SELF, "GVG_030ae")

# Tank Mode (Anodized Robo Cub)
class GVG_030b:
	play = Buff(SELF, "GVG_030be")


# Gift of Mana (Grove Tender)
class GVG_032a:
	play = GainMana(ALL_PLAYERS, 1), FillMana(ALL_PLAYERS, 1)

# Gift of Cards (Grove Tender)
class GVG_032b:
	play = Draw(ALL_PLAYERS)


# Mech-Bear-Cat
class GVG_034:
	events = SELF_DAMAGE.on(Give(CONTROLLER, RandomSparePart()))


# Malorne
class GVG_035:
	deathrattle = Shuffle(CONTROLLER, SELF)


# Druid of the Fang
class GVG_080:
	play = Find(FRIENDLY_MINIONS + BEAST) & Morph(SELF, "GVG_080t")


##
# Spells

# Recycle
class GVG_031:
	play = Shuffle(OPPONENT, TARGET)


# Tree of Life
class GVG_033:
	play = FullHeal(ALL_CHARACTERS)


# Dark Wispers (+5/+5 and Taunt)
class GVG_041a:
	play = Buff(TARGET, "GVG_041c")

# Dark Wispers (Summon 5 Wisps)
class GVG_041b:
	play = Summon(CONTROLLER, "CS2_231") * 5
