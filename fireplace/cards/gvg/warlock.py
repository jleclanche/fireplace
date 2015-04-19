from ..utils import *


##
# Minions

# Mistress of Pain
class GVG_018:
	def DAMAGE(self, source, target, amount):
		if source is self:
			return [Heal(FRIENDLY_HERO, amount)]


# Fel Cannon
class GVG_020:
	OWN_TURN_END = [Hit(RANDOM_MINION - MECH)]


##
# Spells

# Darkbomb
class GVG_015:
	action = [Hit(TARGET, 3)]


# Demonheart
class GVG_019:
	def action(self, target):
		if target.controller == self.controller and target.race == Race.DEMON:
			return [Buff(TARGET, "GVG_019e")]
		else:
			return [Hit(TARGET, 5)]
