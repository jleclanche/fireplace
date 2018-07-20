from ..utils import *


# Luck of the Coin
GAME_001 = buff(health=3)


class GAME_003:
	"""Coin's Vengeance"""
	events = Play(CONTROLLER, MINION).on(Buff(Play.CARD, "GAME_003e"), Destroy(SELF))


GAME_003e = buff(+1, +1)


class GAME_004:
	"""AFK"""
	update = Refresh(CONTROLLER, {GameTag.TIMEOUT: 10})


class GAME_005:
	"""The Coin"""
	play = ManaThisTurn(CONTROLLER, 1)
