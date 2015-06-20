from ..utils import *


##
# Minions

# Snowchugger
class GVG_002:
	events = [
		Damage().on(
			lambda self, target, amount, source: source is self and [Freeze(target)] or []
		)
	]


# Goblin Blastmage
class GVG_004:
	def action(self):
		if self.poweredUp:
			return [Hit(RANDOM_ENEMY_CHARACTER, 1) * 4]


# Illuminator
class GVG_089:
	events = [
		OWN_TURN_END.on(
			lambda self, player: player.secrets and [Heal(FRIENDLY_HERO, 4)] or []
		)
	]


##
# Spells

# Flamecannon
class GVG_001:
	action = [Hit(RANDOM_ENEMY_MINION, 4)]


# Unstable Portal
class GVG_003:
	# TODO
	def action(self):
		card = self.controller.give(RandomMinion())
		self.buff(card, "GVG_003e")


# Echo of Medivh
class GVG_005:
	def action(self):
		return [Give(CONTROLLER, minion.id) for minion in self.controller.field]
