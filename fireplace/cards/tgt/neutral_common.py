from ..utils import *


##
# Minions

class AT_082:
	"""Lowly Squire"""
	inspire = Buff(SELF, "AT_082e")


AT_082e = buff(atk=1)


class AT_083:
	"""Dragonhawk Rider"""
	inspire = Buff(SELF, "AT_083e")


class AT_083e:
	windfury = SET(1)


class AT_084:
	"""Lance Carrier"""
	requirements = {
		PlayReq.REQ_FRIENDLY_TARGET: 0,
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
	play = Buff(TARGET, "AT_084e")


AT_084e = buff(atk=2)


class AT_085:
	"""Maiden of the Lake"""
	update = Refresh(FRIENDLY_HERO_POWER, {GameTag.COST: SET(1)})


class AT_089:
	"""Boneguard Lieutenant"""
	inspire = Buff(SELF, "AT_089e")


AT_089e = buff(health=1)


class AT_090:
	"""Mukla's Champion"""
	inspire = Buff(FRIENDLY_MINIONS, "AT_090e")


AT_090e = buff(+1, +1)


class AT_091:
	"""Tournament Medic"""
	inspire = Heal(FRIENDLY_HERO, 2)


class AT_094:
	"""Flame Juggler"""
	play = Hit(RANDOM_ENEMY_CHARACTER, 1)


class AT_096:
	"""Clockwork Knight"""
	requirements = {
		PlayReq.REQ_FRIENDLY_TARGET: 0,
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
		PlayReq.REQ_TARGET_WITH_RACE: 17}
	play = Buff(TARGET, "AT_096e")


AT_096e = buff(+1, +1)


class AT_100:
	"""Silver Hand Regent"""
	inspire = Summon(CONTROLLER, "CS2_101t")


class AT_103:
	"""North Sea Kraken"""
	requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
	play = Hit(TARGET, 4)


class AT_111:
	"""Refreshment Vendor"""
	play = Heal(ALL_HEROES, 4)


class AT_119:
	"""Kvaldir Raider"""
	inspire = Buff(SELF, "AT_119e")


AT_119e = buff(+2, +2)


class AT_133:
	"""Gadgetzan Jouster"""
	play = JOUST & Buff(SELF, "AT_133e")


AT_133e = buff(+1, +1)
