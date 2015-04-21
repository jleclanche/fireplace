from ..utils import *


##
# Minions

# Goblin Blastmage
class GVG_004:
	def action(self):
		if self.poweredUp:
			return [Hit(RANDOM_ENEMY_CHARACTER, 1) * 4]


# Illuminator
class GVG_089:
	def OWN_TURN_END(self):
		if self.controller.secrets:
			return [Heal(FRIENDLY_HERO, 4)]


##
# Spells

# Flamecannon
class GVG_001:
	action = [Hit(RANDOM_ENEMY_MINION, 4)]


# Unstable Portal
class GVG_003:
	# TODO
	def action(self):
		card = self.controller.give(randomCollectible(type=CardType.MINION))
		self.buff(card, "GVG_003e")


# Echo of Medivh
class GVG_005:
	def action(self):
		return [Give(CONTROLLER, minion.id) for minion in self.controller.field]
