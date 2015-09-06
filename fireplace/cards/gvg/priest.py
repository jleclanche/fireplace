from ..utils import *


##
# Minions

# Shadowbomber
class GVG_009:
	play = Hit(ALL_HEROES, 3)


# Shrinkmeister
class GVG_011:
	play = Buff(TARGET, "GVG_011a")


# Vol'jin
class GVG_014:
	# TODO
	def play(self):
		health = self.target.health
		self.buff(self.target, "GVG_014a", health=self.health)
		self.buff(self, "GVG_014a", health=health)

class GVG_014a:
	max_health = lambda self, i: self.health


# Shadowboxer
class GVG_072:
	events = Heal().on(Hit(RANDOM_ENEMY_CHARACTER, 1))


# Upgraded Repair Bot
class GVG_083:
	# The Enchantment ID is correct
	play = Buff(TARGET, "GVG_069a")

##
# Spells

# Lightbomb
class GVG_008:
	def play(self):
		return [Hit(target, target.atk) for target in self.game.board]


# Velen's Chosen
class GVG_010:
	play = Buff(TARGET, "GVG_010b")


# Light of the Naaru
class GVG_012:
	play = Heal(TARGET, 3), (Attr(TARGET, GameTag.DAMAGE) >= 1) & Summon(CONTROLLER, "EX1_001")
