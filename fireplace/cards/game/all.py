from ..utils import *


# Luck of the Coin
GAME_001 = buff(health=3)


# Coin's Vengeance
class GAME_003:
	events = Play(CONTROLLER, MINION).on(Buff(Play.CARD, "GAME_003e"), Destroy(SELF))

GAME_003e = buff(+1, +1)


# AFK
class GAME_004:
	update = Refresh(CONTROLLER, {GameTag.TIMEOUT: 10})


# The Coin
class GAME_005:
	play = ManaThisTurn(CONTROLLER, 1)
