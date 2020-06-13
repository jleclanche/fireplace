from ..utils import *


##
# Minions

class CFM_315:
	"""Alleycat"""
	play = Summon(CONTROLLER, "CFM_315t")


class CFM_316:
	"""Rat Pack"""
	deathrattle = Summon(CONTROLLER, "CFM_316") * ATK(SELF)


class CFM_333:
	"""Knuckles"""
	events = Attack(SELF, ALL_MINIONS).after(Hit(ENEMY_HERO, ATK(SELF)))


class CFM_335:
	"""Dispatch Kodo"""
	requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
	play = Hit(TARGET, ATK(SELF))


class CFM_336:
	"""Shaky Zipgunner"""
	play = Buff(RANDOM(FRIENDLY_HAND + MINION), "CFM_336e")


CFM_336e = buff(+2, +2)


class CFM_338:
	"""Trogg Beastrager"""
	play = Buff(RANDOM(FRIENDLY_HAND + BEAST), "CFM_338e")


CFM_338e = buff(+1, +1)


##
# Spells

class CFM_026:
	"""Hidden Cache"""
	secret = Play(OPPONENT, MINION).after(
		Reveal(SELF), Buff(RANDOM(FRIENDLY_HAND + MINION), "CFM_026e")
	)


CFM_026e = buff(+2, +2)


class CFM_334:
	"""Smuggler's Crate"""
	play = Buff(RANDOM(FRIENDLY_HAND + BEAST), "CFM_334e")


CFM_334e = buff(+2, +2)


##
# Weapons

class CFM_337:
	"""Piranha Launcher"""
	events = Attack(FRIENDLY_HERO, MINION).after(Summon(CONTROLLER, "CFM_337t"))
