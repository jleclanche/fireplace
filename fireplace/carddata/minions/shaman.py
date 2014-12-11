from ..card import *


# Healing Totem
class NEW1_009(Card):
	def OWN_TURN_END(self):
		targets = self.controller.getTargets(TARGET_FRIENDLY_MINIONS)
		for target in targets:
			self.heal(target, 1)


# Fire Elemental
class CS2_042(Card):
	action = damageTarget(3)


# Dust Devil
class EX1_243(Card):
	Recall = 2


# Earth Elemental
class EX1_250(Card):
	Recall = 3


# Unbound Elemental
class EX1_258(Card):
	def OWN_CARD_PLAYED(self, card):
		if card.overload:
			self.buff("EX1_258e")

class EX1_258e(Card):
	Atk = 1
	Health = 1


# Flametongue Totem
class EX1_565(Card):
	aura = "EX1_565o"

class EX1_565o(Card):
	Atk = 2
	targeting = TARGET_FRIENDLY_MINIONS


# Mana Tide Totem
class EX1_575(Card):
	def OWN_TURN_END(self):
		self.controller.draw()


# Windspeaker
class EX1_587(Card):
	action = buffTarget("EX1_587e")

class EX1_587e(Card):
	windfury = True
