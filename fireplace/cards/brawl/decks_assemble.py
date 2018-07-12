"""
Decks Assemble
"""

from ..utils import *


class TB_010:
	"""Deckbuilding Enchant"""
	events = (
		OWN_TURN_BEGIN.on(DISCOVER(RandomCollectible())),
		Play(CONTROLLER).on(Shuffle(CONTROLLER, Copy(Play.CARD))),
		OWN_TURN_END.on(Shuffle(CONTROLLER, FRIENDLY_HAND))
	)


class TB_011:
	"""Tarnished Coin"""
	play = ManaThisTurn(CONTROLLER, 1)
