from ..utils import *


##
# Minions

class GVG_009:
	"Shadowbomber"
	play = Hit(ALL_HEROES, 3)


class GVG_011:
	"Shrinkmeister"
	play = Buff(TARGET, "GVG_011a")

GVG_011a = buff(atk=-2)


class GVG_014:
	"Vol'jin"
	play = SwapHealth(SELF, TARGET, "GVG_014a")

class GVG_014a:
	max_health = lambda self, i: self.health


class GVG_072:
	"Shadowboxer"
	events = Heal().on(Hit(RANDOM_ENEMY_CHARACTER, 1))


class GVG_083:
	"Upgraded Repair Bot"
	# The Enchantment ID is correct
	play = Buff(TARGET, "GVG_069a")

GVG_069a = buff(health=4)


##
# Spells

class GVG_008:
	"Lightbomb"
	def play(self):
		for target in self.game.board:
			yield Hit(target, target.atk)


class GVG_010:
	"Velen's Chosen"
	play = Buff(TARGET, "GVG_010b")

GVG_010b = buff(+2, +4, spellpower=1)


class GVG_012:
	"Light of the Naaru"
	play = Heal(TARGET, 3), (DAMAGE(TARGET) >= 1) & Summon(CONTROLLER, "EX1_001")
