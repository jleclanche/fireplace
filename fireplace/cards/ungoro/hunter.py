from ..utils import *


##
# Minions

class UNG_800:
	"""Terrorscale Stalker"""
	requirements = {
		PlayReq.REQ_FRIENDLY_TARGET: 0,
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
		PlayReq.REQ_TARGET_WITH_DEATHRATTLE: 0}
	pass


class UNG_912:
	"""Jeweled Macaw"""
	play = Give(CONTROLLER, RandomBeast())


class UNG_913:
	"""Tol'vir Warden"""
	play = ForceDraw(RANDOM(FRIENDLY_DECK + MINION + (COST == 1))) * 2


class UNG_914:
	"""Raptor Hatchling"""
	deathrattle = Shuffle(CONTROLLER, "UNG_914t1")


class UNG_915:
	"""Crackling Razormaw"""
	requirements = {
		PlayReq.REQ_FRIENDLY_TARGET: 0,
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
		PlayReq.REQ_TARGET_WITH_RACE: 20}
	play = Adapt(TARGET)


class UNG_919:
	"""Swamp King Dred"""
	events = Play(OPPONENT, MINION).after(
		Find(Play.CARD + IN_PLAY - DEAD) & (
			Find(SELF - FROZEN) &
			Attack(SELF, Play.CARD)
		)
	)


##
# Spells

class UNG_910:
	"""Grievous Bite"""
	requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
	play = Hit(TARGET, 2), Hit(TARGET_ADJACENT, 1)


class UNG_916:
	"""Stampede"""
	play = Buff(CONTROLLER, "UNG_916e")


class UNG_916e:
	events = Play(CONTROLLER, BEAST).after(Give(CONTROLLER, RandomBeast()))


class UNG_917:
	"""Dinomancy"""
	play = Summon(CONTROLLER, "UNG_917t1")


class UNG_917t1:
	requirements = {
		PlayReq.REQ_TARGET_TO_PLAY: 0,
		PlayReq.REQ_TARGET_WITH_RACE: 20,
	}
	activate = Buff(TARGET, "UNG_917e")


UNG_917e = buff(+2, +2)


class UNG_920:
	"""The Marsh Queen"""
	progress_total = 7
	quest = Play(CONTROLLER, MINION + (COST == 1)).after(AddProgress(SELF, Play.CARD))
	reward = Give(CONTROLLER, "UNG_920t1")


class UNG_920t1:
	play = Shuffle(CONTROLLER, "UNG_920t2") * 15


class UNG_920t2:
	play = Draw(CONTROLLER)
