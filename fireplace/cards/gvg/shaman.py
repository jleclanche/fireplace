from ..utils import *


##
# Minions

# Vitality Totem
class GVG_039:
	OWN_TURN_END = [Heal(FRIENDLY_HERO, 4)]


# Siltfin Spiritwalker
class GVG_040:
	def OWN_MINION_DESTROY(self, minion):
		if minion.race == Race.MURLOC:
			return [Draw(CONTROLLER, 1)]


##
# Spells

# Ancestor's Call
class GVG_029:
	action = [
		ForcePlay(CONTROLLER, RANDOM(CONTROLLER_HAND + MINION)),
		ForcePlay(OPPONENT, RANDOM(OPPONENT_HAND + MINION)),
	]


# Crackle
class GVG_038:
	def action(self, target):
		return [Hit(TARGET, random.randint(3, 6))]


##
# Weapons

# Powermace
class GVG_036:
	action = [Buff(RANDOM(FRIENDLY_MINIONS + MECH), "GVG_036e")]
