from ..utils import *


##
# Minions

# Shadowbomber
class GVG_009:
	play = Hit(ALL_HEROES, 3)


# Shrinkmeister
class GVG_011:
	play = Buff(TARGET, "GVG_011a")

GVG_011a = buff(atk=-2)


# Vol'jin
class GVG_014:
	play = SwapHealth(SELF, TARGET, "GVG_014a")

class GVG_014a:
	max_health = lambda self, i: self.health


# Shadowboxer
class GVG_072:
	events = Heal().on(Hit(RANDOM_ENEMY_CHARACTER, 1))


# Upgraded Repair Bot
class GVG_083:
	# The Enchantment ID is correct
	play = Buff(TARGET, "GVG_069a")

GVG_069a = buff(health=4)


##
# Spells

# Lightbomb
class GVG_008:
	def play(self):
		for target in self.game.board:
			yield Hit(target, target.atk)


# Velen's Chosen
class GVG_010:
	play = Buff(TARGET, "GVG_010b")

GVG_010b = buff(+2, +4, spellpower=1)


# Light of the Naaru
class GVG_012:
	play = Heal(TARGET, 3), (DAMAGE(TARGET) >= 1) & Summon(CONTROLLER, "EX1_001")
