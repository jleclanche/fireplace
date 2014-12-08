from ..card import *
from fireplace.enums import CardType


# Archmage Antonidas
class EX1_559(Card):
	def OWN_CARD_PLAYED(self, card):
		if card.type == CardType.SPELL:
			self.controller.give("CS2_029")
