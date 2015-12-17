"""
Boom Bot vs. Annoy-o-Tron!
"""

from ..utils import *


# Hello! Hello! Hello!
class TB_MechWar_Boss1_HeroPower:
	activate = SetTag(LOWEST_ATK(FRIENDLY_MINIONS), (GameTag.TAUNT, GameTag.DIVINE_SHIELD))


# Boom Bot Jr.
class TB_MechWar_Boss2_HeroPower:
	activate = Hit(RANDOM_ENEMY_CHARACTER, 1) * 2
