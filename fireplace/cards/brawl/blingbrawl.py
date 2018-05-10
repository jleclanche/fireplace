"""
Blingtron's Beauteous Brawl
"""
from ..utils import *


class TP_Bling_HP2:
	"""Cash In"""
	activate = Destroy(FRIENDLY_WEAPON)


class TB_BlingBrawl_Blade1e:
	"""Blingtron's Blade"""
	events = Death(OWNER).on(Summon(CONTROLLER, RandomWeapon()))


class TB_BlingBrawl_Blade2:
	"""Blingtron's Blade HERO"""
	events = Summon(CONTROLLER, WEAPON).on(
		Buff(Summon.CARD, "TB_BlingBrawl_Blade1e")
	)


class TB_BlingBrawl_Hero1p:
	"""Sharpen (Unused)"""
	activate = Buff(FRIENDLY_WEAPON, "TB_BlingBrawl_Hero1e")


TB_BlingBrawl_Hero1e = buff(atk=1)
