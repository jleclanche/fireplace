from ..utils import *


##
# Minions

# Hobgoblin
class GVG_104:
	def OWN_CARD_PLAYED(self, card):
		if card.type == CardType.MINION and card.atk == 1:
			return [Buff(card, "GVG_104a")]


# Piloted Sky Golem
class GVG_105:
	def deathrattle(self):
		return [Summon(CONTROLLER, randomCollectible(type=CardType.MINION, cost=4))]


# Junkbot
class GVG_106:
	def OWN_MINION_DESTROY(self, minion):
		if minion.race == Race.MECHANICAL:
			return [Buff(SELF, "GVG_106e")]


# Enhance-o Mechano
class GVG_107:
	def action(self):
		for target in self.controller.field:
			tag = random.choice((GameTag.WINDFURY, GameTag.TAUNT, GameTag.DIVINE_SHIELD))
			yield SetTag(target, {tag: True})
