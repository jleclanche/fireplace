"""
Unite Against Mechazod!
"""

from ..utils import *


MECHAZOD = (
	ID("HRW02_1") |
	ID("TB_CoOp_Mechazod") |
	ID("TB_CoOp_Mechazod_V2") |
	ID("TB_CoOp_Mechazod2")
)

ALL_MINIONS = ALL_MINIONS - MECHAZOD


class TB_CoOp_Mechazod:
	"""Gearmaster Mechazod"""
	events = (
		EndTurn().on((Count(ENEMY_MINIONS) == 7) & Destroy(ENEMY_MINIONS)),
		BeginTurn().on(Steal(BeginTurn.PLAYER, SELF))
	)


# Gearmastet Mechazod (old version?)
HRW02_1 = TB_CoOp_Mechazod

# Gearmaster Mechazod (v2?)
TB_CoOp_Mechazod_V2 = TB_CoOp_Mechazod

# Overloaded Mechazod (unused?)


class TB_CoOp_Mechazod2(TB_CoOp_Mechazod):
	"""Overloaded Mechazod"""


class TB_CoOpBossSpell_1:
	"""Prioritize"""
	play = Hit(HIGHEST_ATK(ALL_MINIONS), ATK(MECHAZOD))


class TB_CoOpBossSpell_2:
	"""Bomb Salvo"""
	play = Hit(RANDOM(ALL_CHARACTERS - MECHAZOD) * 3, ATK(MECHAZOD))


class TB_CoOpBossSpell_3:
	"""Release Coolant"""
	play = Hit(ALL_MINIONS, ATK(MECHAZOD)), Freeze(ALL_MINIONS)


class TB_CoOpBossSpell_4:
	"""Overclock"""
	play = Buff(MECHAZOD, "HRW02_1e")


HRW02_1e = buff(atk=2)


class TB_CoOpBossSpell_5:
	"""Double Zap"""
	play = Hit(ALL_HEROES, ATK(MECHAZOD))


class TB_CoOpBossSpell_6:
	"""Kill the Lorewalker"""
	play = Destroy(ID("EX1_100")[0])
