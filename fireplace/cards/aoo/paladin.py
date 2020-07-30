from ..utils import *


##
# Minions

class BT_020:
	"""Aldor Attendant"""
	play = Buff(CONTROLLER, "BT_020e")


class BT_020e:
	update = Refresh(FRIENDLY + LIBRAMS, {GameTag.COST: -1})


class BT_009:
	"""Imprisoned Sungill"""
	dormant = 2
	awaken = Summon(CONTROLLER, "BT_009t") * 2


class BT_019:
	"""Murgur Murgurgle"""
	deathrattle = Shuffle(CONTROLLER, "BT_019t")


class BT_019t:
	play = Summon(CONTROLLER, RandomMinion(race=Race.MURLOC)).then(
		GiveDivineShield(Shuffle.CARD)) * 4


class BT_026:
	"""Aldor Truthseeker"""
	play = Buff(CONTROLLER, "BT_026e")


class BT_026e:
	update = Refresh(FRIENDLY + LIBRAMS, {GameTag.COST: -2})


class BT_334:
	play = Give(CONTROLLER, Copy(SPELL + CAST_ON_FRIENDLY_CHARACTERS))


##
# Spells

class BT_025:
	"""Libram of Wisdom"""
	requirements = {
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_FRIENDLY_TARGET: 0,
		PlayReq.REQ_TARGET_TO_PLAY: 0
	}
	play = Buff(TARGET, "BT_025e")


class BT_025e:
	deathrattle = Give(CONTROLLER, "BT_025")
	tags = {
		GameTag.ATK: +1,
		GameTag.HEALTH: +1,
		GameTag.DEATHRATTLE: True
	}


class BT_292:
	"""Hand of A'dal"""
	requirements = {
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_TARGET_TO_PLAY: 0}
	play = Buff(TARGET, "BT_292e"), Draw(CONTROLLER)


BT_292e = buff(atk=2, health=2)


class BT_011:
	"""Libram of Justice"""
	play = Summon(CONTROLLER, "BT_011t"), Buff(ENEMY_MINIONS, "BT_011e")


class BT_011e:
	max_health = SET(1)


class BT_024:
	"""Libram of Hope"""
	requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
	play = Heal(TARGET, 8), Summon(CONTROLLER, "BT_024t")


##
# Weapons

class BT_018:
	"""Underlight Angling Rod"""
	events = Attack(FRIENDLY_HERO).after(Give(CONTROLLER, RandomMinion(race=Race.MURLOC)))
