from ..utils import *


##
# Minions

class GVG_020:
	"""Fel Cannon"""
	events = OWN_TURN_END.on(Hit(RANDOM(ALL_MINIONS - MECH), 2))


class GVG_021:
	"""Mal'Ganis"""
	update = (
		Refresh(FRIENDLY_MINIONS + DEMON - SELF, buff="GVG_021e"),
		Refresh(FRIENDLY_HERO, {GameTag.CANT_BE_DAMAGED: True}),
	)


GVG_021e = buff(+2, +2)


class GVG_077:
	"""Anima Golem"""
	events = TURN_END.on(Find(FRIENDLY_MINIONS - SELF) | Destroy(SELF))


class GVG_100:
	"""Floating Watcher"""
	events = Damage(FRIENDLY_HERO).on(CurrentPlayer(CONTROLLER) & Buff(SELF, "GVG_100e"))


GVG_100e = buff(+2, +2)


##
# Spells

class GVG_015:
	"""Darkbomb"""
	requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
	play = Hit(TARGET, 3)


class GVG_019:
	"""Demonheart"""
	requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
	play = Find(TARGET + FRIENDLY + DEMON) & Buff(TARGET, "GVG_019e") | Hit(TARGET, 5)


GVG_019e = buff(+5, +5)


class GVG_045:
	"""Imp-losion"""
	requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
	play = Summon(CONTROLLER, "GVG_045t") * Hit(TARGET, RandomNumber(2, 3, 4))
