"""
Decks Assemble
"""

from ..utils import *


# Deckbuilding Enchant
class TB_010:
	events = (
		OWN_TURN_BEGIN.on(DISCOVER(RandomCollectible())),
		Play(CONTROLLER).on(Shuffle(CONTROLLER, Copy(Play.CARD))),
		OWN_TURN_END.on(Shuffle(CONTROLLER, FRIENDLY_HAND))
	)

# Tarnished Coin
class TB_011:
	play = ManaThisTurn(CONTROLLER, 1)
