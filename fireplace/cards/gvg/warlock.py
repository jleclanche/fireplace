from ..utils import *


##
# Minions

# Mistress of Pain
class GVG_018:
	events = Damage().on(
		lambda self, target, amount, source: source is self and Heal(FRIENDLY_HERO, amount)
	)


# Fel Cannon
class GVG_020:
	events = OWN_TURN_END.on(Hit(RANDOM(ALL_MINIONS - MECH), 2))


# Anima Golem
class GVG_077:
	events = TURN_END.on(Find(FRIENDLY_MINIONS - SELF) | Destroy(SELF))


# Floating Watcher
class GVG_100:
	events = Damage(FRIENDLY_HERO).on(
		lambda self, target, amount, source: self.controller.current_player and Buff(SELF, "GVG_100e")
	)


##
# Spells

# Darkbomb
class GVG_015:
	play = Hit(TARGET, 3)


# Demonheart
class GVG_019:
	def play(self, target):
		if target.controller == self.controller and target.race == Race.DEMON:
			return Buff(TARGET, "GVG_019e")
		else:
			return Hit(TARGET, 5)
