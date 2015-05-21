from ..utils import *


##
# Minions

# Mistress of Pain
class GVG_018:
	events = [
		Damage().on(
			lambda self, source, target, amount: source is self and [Heal(FRIENDLY_HERO, amount)] or []
		)
	]


# Fel Cannon
class GVG_020:
	events = [
		OWN_TURN_END.on(Hit(RANDOM(ALL_MINIONS - MECH), 2))
	]


# Anima Golem
class GVG_077:
	events = [
		TURN_END.on(
			lambda self, player: self.controller.field != [self] and [Destroy(SELF)] or []
		)
	]


# Floating Watcher
class GVG_100:
	events = [
		Damage(FRIENDLY_HERO).on(
			lambda self, target, amount, source: self.controller.currentPlayer and [Buff(SELF, "GVG_100e")] or []
		)
	]


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
