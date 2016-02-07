"""
Blingtron's Beauteous Brawl
"""
from ..utils import *


# Cash In
class TP_Bling_HP2:
	activate = Destroy(FRIENDLY_WEAPON)


# Blingtron's Blade
class TB_BlingBrawl_Blade1e:
	events = Death(OWNER).on(Summon(CONTROLLER, RandomWeapon()))


# Blingtron's Blade HERO
class TB_BlingBrawl_Blade2:
	events = Summon(CONTROLLER, WEAPON).on(
		Buff(Summon.CARD, "TB_BlingBrawl_Blade1e")
	)


# Sharpen (Unused)
class TB_BlingBrawl_Hero1p:
	activate = Buff(FRIENDLY_WEAPON, "TB_BlingBrawl_Hero1e")

TB_BlingBrawl_Hero1e = buff(atk=1)
