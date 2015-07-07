from ..utils import *


##
# Minions

# Attack Mode (Anodized Robo Cub)
class GVG_030a:
	action = [Buff(SELF, "GVG_030ae")]

# Tank Mode (Anodized Robo Cub)
class GVG_030b:
	action = [Buff(SELF, "GVG_030be")]


# Gift of Mana (Grove Tender)
class GVG_032a:
	action = [GainMana(ALL_PLAYERS, 1), FillMana(ALL_PLAYERS, 1)]

# Gift of Cards (Grove Tender)
class GVG_032b:
	action = [Draw(ALL_PLAYERS)]


# Malorne
class GVG_035:
	deathrattle = [Shuffle(CONTROLLER, SELF)]


# Druid of the Fang
class GVG_080:
	def action(self):
		if self.powered_up:
			return [Morph(SELF, "GVG_080t")]


##
# Spells

# Recycle
class GVG_031:
	action = [Shuffle(OPPONENT, TARGET)]


# Tree of Life
class GVG_033:
	action = [FullHeal(ALL_CHARACTERS)]


# Dark Wispers (+5/+5 and Taunt)
class GVG_041a:
	action = [Buff(TARGET, "GVG_041c")]

# Dark Wispers (Summon 5 Wisps)
class GVG_041b:
	action = [Summon(CONTROLLER, "CS2_231") * 5]
