"""
Battle of the Builds
"""

from ..utils import *


# Spell Bonus
class TB_PickYourFate_8:
	play = Buff(CONTROLLER, "TB_PickYourFate_8_Ench")

class TB_PickYourFate_8_Ench:
	events = OWN_SPELL_PLAY.on(GainArmor(FRIENDLY_HERO, 3))


# Deathrattle Bonus
class TB_PickYourFate_9:
	play = Buff(CONTROLLER, "TB_PickYourFate_9_Ench")

class TB_PickYourFate_9_Ench:
	update = Refresh(FRIENDLY_MINIONS + DEATHRATTLE, "TB_PickYourFate_9_EnchMinion")

TB_PickYourFate_9_EnchMinion = buff(+1, +1)


# Battlecry Bonus
class TB_PickYourFate_10:
	play = Buff(CONTROLLER, "TB_PickYourFate_10_Ench")

class TB_PickYourFate_10_Ench:
	update = Refresh(FRIENDLY_MINIONS + BATTLECRY, "TB_PickYourFate_10_EnchMinion")

TB_PickYourFate_10_EnchMinion = buff(+1, +1)


# Murloc Bonus
class TB_PickYourFate_11b:
	play = Buff(CONTROLLER, "TB_PickYourFate_11_Ench")

class TB_PickYourFate_11_Ench:
	events = OWN_TURN_END.on(Summon(CONTROLLER, "LOEA10_3"))
