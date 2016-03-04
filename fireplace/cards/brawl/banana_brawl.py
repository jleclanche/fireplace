"""
Banana Brawl
"""

from ..utils import *


RandomBanana = RandomID("EX1_014t", "TB_006", "TB_007", "TB_008")


# Big Banana
class TB_006:
	play = Buff(TARGET, "TB_006e")

TB_006e = buff(+2, +2)


# Deviate Banana
class TB_007:
	play = Buff(TARGET, "TB_007e")

TB_007e = AttackHealthSwapBuff()


# Rotten Banana
class TB_008:
	play = Hit(TARGET, 1)
