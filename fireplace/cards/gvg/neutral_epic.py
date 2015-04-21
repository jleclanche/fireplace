from ..utils import *


##
# Minions

# Hobgoblin
class GVG_104:
	def OWN_CARD_PLAYED(self, card):
		if card.type == CardType.MINION and card.atk == 1:
			return [Buff(card, "GVG_104a")]
