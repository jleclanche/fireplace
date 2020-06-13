from ..utils import *


##
# Minions

class AT_086:
	"""Saboteur"""
	play = Buff(OPPONENT, "AT_086e")


class AT_086e:
	update = CurrentPlayer(OWNER) & Refresh(ENEMY_HERO_POWER, {GameTag.COST: +5})
	events = OWN_TURN_BEGIN.on(Destroy(SELF))


class AT_088:
	"""Mogor's Champion"""
	events = FORGETFUL


class AT_105:
	"""Injured Kvaldir"""
	play = Hit(SELF, 3)


class AT_106:
	"""Light's Champion"""
	requirements = {
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
		PlayReq.REQ_TARGET_WITH_RACE: 15}
	play = Silence(TARGET)


class AT_108:
	"""Armored Warhorse"""
	play = JOUST & GiveCharge(SELF)


class AT_109:
	"""Argent Watchman"""
	inspire = Buff(SELF, "AT_109e")


AT_109e = buff(cant_attack=False)


class AT_110:
	"""Coliseum Manager"""
	inspire = Bounce(SELF)


class AT_112:
	"""Master Jouster"""
	play = JOUST & SetTag(SELF, (GameTag.TAUNT, GameTag.DIVINE_SHIELD))


class AT_115:
	"""Fencing Coach"""
	requirements = {PlayReq.REQ_MINION_TARGET: 0}
	play = Buff(CONTROLLER, "AT_115e")


class AT_115e:
	update = Refresh(FRIENDLY_HERO_POWER, {GameTag.COST: -2})
	events = Activate(CONTROLLER, HERO_POWER).on(Destroy(SELF))
