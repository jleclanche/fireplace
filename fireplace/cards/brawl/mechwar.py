"""
Boom Bot vs. Annoy-o-Tron!
"""

from ..utils import *


class TB_MechWar_Boss1_HeroPower:
	"""Hello! Hello! Hello!"""
	requirements = {PlayReq.REQ_FRIENDLY_TARGET: 0, PlayReq.REQ_MINION_TARGET: 0}
	activate = SetTag(LOWEST_ATK(FRIENDLY_MINIONS), (GameTag.TAUNT, GameTag.DIVINE_SHIELD))


class TB_MechWar_Boss2_HeroPower:
	"""Boom Bot Jr."""
	activate = Hit(RANDOM_ENEMY_CHARACTER, 1) * 2
