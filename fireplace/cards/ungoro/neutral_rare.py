from ..utils import *


##
# Minions

class UNG_002:
	"""Volcanosaur"""
	play = Adapt(SELF), Adapt(SELF)


class UNG_070:
	"""Tol'vir Stoneshaper"""
	play = PLAYED_ELEMENTAL_LAST_TURN(CONTROLLER) & (Taunt(SELF), GiveDivineShield(SELF))


class UNG_072:
	"""Stonehill Defender"""
	play = DISCOVER(RandomMinion(taunt=True))


class UNG_075:
	"""Vicious Fledgling"""
	events = Attack(SELF, ALL_HEROES).after(Adapt(SELF))


class UNG_079:
	"""Frozen Crusher"""
	events = Attack(SELF).after(Freeze(SELF))


class UNG_083:
	"""Devilsaur Egg"""
	deathrattle = Summon(CONTROLLER, "UNG_083t1")


class UNG_807:
	"""Golakka Crawler"""
	play = Destroy(TARGET), Buff(SELF, "UNG_807e")


UNG_807e = buff(+1, +1)


class UNG_816:
	"""Servant of Kalimos"""
	play = DISCOVER(RandomElemental())
