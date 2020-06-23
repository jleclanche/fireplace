from ..utils import *


##
# Minions

class GVG_039:
	"""Vitality Totem"""
	events = OWN_TURN_END.on(Heal(FRIENDLY_HERO, 4))


class GVG_040:
	"""Siltfin Spiritwalker"""
	events = Death(FRIENDLY + MURLOC).on(Draw(CONTROLLER))


class GVG_042:
	"""Neptulon"""
	play = Give(CONTROLLER, RandomMurloc()) * 4


class GVG_066:
	"""Dunemaul Shaman"""
	events = FORGETFUL


##
# Spells

class GVG_029:
	"""Ancestor's Call"""
	play = (
		Summon(CONTROLLER, RANDOM(FRIENDLY_HAND + MINION)),
		Summon(OPPONENT, RANDOM(ENEMY_HAND + MINION)),
	)


class GVG_038:
	"""Crackle"""
	requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
	play = Hit(TARGET, RandomNumber(3, 4, 5, 6))


##
# Weapons

class GVG_036:
	"""Powermace"""
	deathrattle = Buff(RANDOM(FRIENDLY_MINIONS + MECH), "GVG_036e")


GVG_036e = buff(+2, +2)
