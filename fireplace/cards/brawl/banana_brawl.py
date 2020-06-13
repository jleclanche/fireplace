"""
Banana Brawl
"""

from ..utils import *


RandomBanana = RandomID("EX1_014t", "TB_006", "TB_007", "TB_008")


class TB_006:
	"""Big Banana"""
	requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
	play = Buff(TARGET, "TB_006e")


TB_006e = buff(+2, +2)


class TB_007:
	"""Deviate Banana"""
	requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
	play = Buff(TARGET, "TB_007e")


TB_007e = AttackHealthSwapBuff()


class TB_008:
	"""Rotten Banana"""
	requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
	play = Hit(TARGET, 1)
