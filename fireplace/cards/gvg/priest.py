from ..utils import *


##
# Minions

# Shadowbomber
class GVG_009:
	action = [Hit(ALL_HEROES, 3)]


# Shrinkmeister
class GVG_011:
	action = [Buff(TARGET, "GVG_011a")]


# Vol'jin
class GVG_014:
	# TODO
	def action(self, target):
		health = target.health
		self.buff(target, "GVG_014a", health=self.health)
		self.buff(self, "GVG_014a", health=health)

class GVG_014a:
	max_health = lambda self, i: self.health


# Shadowboxer
class GVG_072:
	events = [
		Heal().on(Hit(RANDOM_ENEMY_CHARACTER, 1))
	]


# Upgraded Repair Bot
class GVG_083:
	# The Enchantment ID is correct
	action = [Buff(TARGET, "GVG_069a")]

##
# Spells

# Lightbomb
class GVG_008:
	def action(self):
		return [Hit(target, target.atk) for target in self.game.board]


# Velen's Chosen
class GVG_010:
	action = [Buff(TARGET, "GVG_010b")]


# Light of the Naaru
class GVG_012:
	def action(self, target):
		yield Heal(TARGET, 3)
		if target.damage:
			yield Summon(CONTROLLER, "EX1_001")
