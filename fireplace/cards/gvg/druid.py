from ..utils import *


##
# Minions

# Anodized Robo Cub
class GVG_030:
	choose = ("GVG_030a", "GVG_030b")

class GVG_030a:
	play = Buff(SELF, "GVG_030ae")

GVG_030ae = buff(atk=1)

class GVG_030b:
	play = Buff(SELF, "GVG_030be")

GVG_030be = buff(health=1)


# Grove Tender
class GVG_032:
	choose = ("GVG_032a", "GVG_032b")

class GVG_032a:
	play = GainMana(ALL_PLAYERS, 1)

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
	powered_up = Find(FRIENDLY_MINIONS + BEAST)
	play = powered_up & Morph(SELF, "GVG_080t")


##
# Spells

# Recycle
class GVG_031:
	play = Shuffle(OPPONENT, TARGET)


# Tree of Life
class GVG_033:
	play = FullHeal(ALL_CHARACTERS)


# Dark Wispers
class GVG_041:
	choose = ("GVG_041a", "GVG_041b")

class GVG_041a:
	play = Buff(TARGET, "GVG_041c")

GVG_041c = buff(+5, +5, taunt=True)

class GVG_041b:
	play = Summon(CONTROLLER, "CS2_231") * 5
