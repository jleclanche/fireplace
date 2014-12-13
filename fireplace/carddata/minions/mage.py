from ..card import *
from fireplace.enums import CardType


# Archmage Antonidas
class EX1_559(Card):
	def OWN_CARD_PLAYED(self, card):
		if card.type == CardType.SPELL:
			self.controller.give("CS2_029")


# Mana Wyrm
class NEW1_012(Card):
	def OWN_CARD_PLAYED(self, card):
		if card.type == CardType.SPELL:
			self.buff("NEW1_012o")

class NEW1_012o(Card):
	Atk = 1
