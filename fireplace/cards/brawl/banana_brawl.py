"""
Banana Brawl
"""

from ..utils import *


RandomBanana = RandomID("EX1_014t", "TB_006", "TB_007", "TB_008")


class TB_006:
	"Big Banana"
	play = Buff(TARGET, "TB_006e")

TB_006e = buff(+2, +2)


class TB_007:
	"Deviate Banana"
	play = Buff(TARGET, "TB_007e")

TB_007e = AttackHealthSwapBuff()


class TB_008:
	"Rotten Banana"
	play = Hit(TARGET, 1)
