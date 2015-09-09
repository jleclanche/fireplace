"""
GAME set and other special cards
"""
from ..utils import *


# AFK
class GAME_004:
	update = Refresh(CONTROLLER, {GameTag.TIMEOUT: 10})


# The Coin
class GAME_005:
	play = ManaThisTurn(CONTROLLER, 1)


# Big Banana
class TB_006:
	play = Buff(TARGET, "TB_006e")


# Deviate Banana
class TB_007:
	play = SwapAttackAndHealth(TARGET, "TB_007e")


# Rotten Banana
class TB_008:
	play = Hit(TARGET, 1)


# Mysterious Pilot
class TB_Pilot1:
	deathrattle = Summon(CONTROLLER, RandomMinion(cost=Attr(SELF, GameTag.COST)))
