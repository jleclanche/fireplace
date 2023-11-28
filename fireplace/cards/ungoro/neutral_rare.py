from ..utils import *


##
# Minions

class UNG_002:
	"""Volcanosaur"""
	play = Adapt(SELF) * 2


class UNG_070:
	"""Tol'vir Stoneshaper"""
	play = ELEMENTAL_PLAYED_LAST_TURN & (Buff(SELF, "UNG_070e"), GiveDivineShield(SELF))


UNG_070e = buff(taunt=True)


class UNG_072:
	"""Stonehill Defender"""
	play = DISCOVER(RandomMinion(taunt=True))


class UNG_075:
	"""Vicious Fledgling"""
	events = Attack(SELF).after(Adapt(SELF))


class UNG_079:
	"""Frozen Crusher"""
	events = Attack(SELF).after(Freeze(SELF))


class UNG_083:
	"""Devilsaur Egg"""
	deathrattle = Summon(CONTROLLER, "UNG_083t1")


class UNG_807:
	"""Golakka Crawler"""
	requirements = {
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
		PlayReq.REQ_TARGET_WITH_RACE: 23}
	play = Destroy(TARGET), Buff(SELF, "UNG_807e")


UNG_807e = buff(+2, +2)


class UNG_816:
	"""Servant of Kalimos"""
	requirements = {
		PlayReq.REQ_FRIENDLY_TARGET: 0,
		PlayReq.REQ_TARGET_WITH_DEATHRATTLE: 0}
	pass


class UNG_844:
	"""Humongous Razorleaf"""
	play = ELEMENTAL_PLAYED_LAST_TURN & DISCOVER(RandomElemental())
