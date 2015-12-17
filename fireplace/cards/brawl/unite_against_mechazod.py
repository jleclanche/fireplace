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


# Gearmaster Mechazod
class TB_CoOp_Mechazod:
	events = (
		EndTurn().on((Count(ENEMY_MINIONS) == 7) & Destroy(ENEMY_MINIONS)),
		BeginTurn().on(Steal(BeginTurn.PLAYER, SELF))
	)


# Gearmastet Mechazod (old version?)
HRW02_1 = TB_CoOp_Mechazod

# Gearmaster Mechazod (v2?)
TB_CoOp_Mechazod_V2 = TB_CoOp_Mechazod

# Overloaded Mechazod (unused?)
TB_CoOp_Mechazod2 = TB_CoOp_Mechazod


# Prioritize
class TB_CoOpBossSpell_1:
	play = Hit(HIGHEST_ATK(ALL_MINIONS), ATK(MECHAZOD))


# Bomb Salvo
class TB_CoOpBossSpell_2:
	play = Hit(RANDOM(ALL_CHARACTERS - MECHAZOD) * 3, ATK(MECHAZOD))


# Release Coolant
class TB_CoOpBossSpell_3:
	play = Hit(ALL_MINIONS, ATK(MECHAZOD)), Freeze(ALL_MINIONS)


# Overclock
class TB_CoOpBossSpell_4:
	play = Buff(MECHAZOD, "HRW02_1e")

HRW02_1e = buff(atk=2)


# Double Zap
class TB_CoOpBossSpell_5:
	play = Hit(ALL_HEROES, ATK(MECHAZOD))


# Kill the Lorewalker
class TB_CoOpBossSpell_6:
	play = Destroy(ID("EX1_100"))
