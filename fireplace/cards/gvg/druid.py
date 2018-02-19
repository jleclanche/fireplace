from ..utils import *


##
# Minions

class GVG_030:
	"Anodized Robo Cub"
	choose = ("GVG_030a", "GVG_030b")
	play = ChooseBoth(CONTROLLER) & (Buff(SELF, "GVG_030ae"), Buff(SELF, "GVG_030be"))

class GVG_030a:
	play = Buff(SELF, "GVG_030ae")

GVG_030ae = buff(atk=1)

class GVG_030b:
	play = Buff(SELF, "GVG_030be")

GVG_030be = buff(health=1)


class GVG_032:
	"Grove Tender"
	choose = ("GVG_032a", "GVG_032b")
	play = ChooseBoth(CONTROLLER) & (GainMana(ALL_PLAYERS, 1), Draw(ALL_PLAYERS))

class GVG_032a:
	play = GainMana(ALL_PLAYERS, 1)

class GVG_032b:
	play = Draw(ALL_PLAYERS)


class GVG_034:
	"Mech-Bear-Cat"
	events = SELF_DAMAGE.on(Give(CONTROLLER, RandomSparePart()))


class GVG_035:
	"Malorne"
	deathrattle = Shuffle(CONTROLLER, SELF)


class GVG_080:
	"Druid of the Fang"
	powered_up = Find(FRIENDLY_MINIONS + BEAST)
	play = powered_up & Morph(SELF, "GVG_080t")


##
# Spells

class GVG_031:
	"Recycle"
	play = Shuffle(OPPONENT, TARGET)


class GVG_033:
	"Tree of Life"
	play = FullHeal(ALL_CHARACTERS)


class GVG_041:
	"Dark Wispers"
	choose = ("GVG_041a", "GVG_041b")
	play = ChooseBoth(CONTROLLER) & (Buff(TARGET, "GVG_041c"), Summon(CONTROLLER, "CS2_231") * 5)

class GVG_041a:
	play = Buff(TARGET, "GVG_041c")

GVG_041c = buff(+5, +5, taunt=True)

class GVG_041b:
	play = Summon(CONTROLLER, "CS2_231") * 5
