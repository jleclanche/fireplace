"""
Cards used in the Tutorial missions
"""
from ..utils import *


##
# Hero Powers

class TU4d_003:
	"""Shotgun Blast"""
	requirements = {PlayReq.REQ_ENEMY_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
	activate = Hit(TARGET, 1)


class TU4e_002:
	"""Flames of Azzinoth"""
	requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 2}
	activate = Summon(CONTROLLER, "TU4e_002t") * 2


##
# Minions

class TU4c_003:
	"""Barrel (Unused)"""
	deathrattle = Summon(OPPONENT, "TU4c_005")


class TU4f_007:
	"""Crazy Monkey"""
	play = Give(OPPONENT, "TU4c_006")


class TU4c_006:
	requirements = {
		PlayReq.REQ_FRIENDLY_TARGET: 0,
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_TARGET_TO_PLAY: 0}
	play = Buff(TARGET, "TU4c_006e")


# Bananas
TU4c_006e = buff(+1, +1)


##
# Spells

class TU4a_004:
	"""Hogger SMASH!"""
	requirements = {
		PlayReq.REQ_ENEMY_TARGET: 0,
		PlayReq.REQ_HERO_TARGET: 0,
		PlayReq.REQ_TARGET_TO_PLAY: 0}
	play = Hit(TARGET, 4)


class TU4c_002:
	"""Barrel Toss"""
	requirements = {PlayReq.REQ_ENEMY_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
	play = Hit(TARGET, 2)


class TU4c_004:
	"""Stomp"""
	play = Hit(ENEMY_CHARACTERS, 2)


class TU4c_008:
	"""Will of Mukla"""
	play = Heal(FRIENDLY_HERO, 8)


# Might of Mukla (Unused)
TU4c_008e = buff(atk=8)


class TU4e_005:
	"""Flame Burst"""
	play = Hit(RANDOM_ENEMY_CHARACTER, 1) * 5


class TU4f_004:
	"""Legacy of the Emperor"""
	play = Buff(FRIENDLY_MINIONS, "TU4f_004o")


TU4f_004o = buff(+2, +2)


class TU4f_006:
	"""Transcendence"""
	play = Buff(FRIENDLY_HERO, "TU4f_006o")


class TU4f_006o:
	"""Transcendence"""
	events = Death(FRIENDLY + MINION).on(
		Find(FRIENDLY_MINIONS) | Destroy(SELF)
	)

	tags = {
		GameTag.CANT_BE_ATTACKED: True,
		GameTag.CANT_BE_TARGETED_BY_OPPONENTS: True,
	}
