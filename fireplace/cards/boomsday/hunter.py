from ..utils import *


##
# Minions

class BOT_034:
	"""Boommaster Flark"""
	pass


class BOT_035:
	"""Venomizer"""
	pass


class BOT_038:
	"""Fireworks Tech"""
	requirements = {
		PlayReq.REQ_FRIENDLY_TARGET: 0,
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
		PlayReq.REQ_TARGET_WITH_RACE: 17}
	pass


class BOT_039:
	"""Necromechanic"""
	pass


class BOT_251:
	"""Spider Bomb"""
	pass


##
# Spells

class BOT_033:
	"""Bomb Toss"""
	requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
	pass


class BOT_402:
	"""Secret Plan"""
	pass


class BOT_429:
	"""Flark's Boom-Zooka"""
	requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
	pass


class BOT_437:
	"""Goblin Prank"""
	requirements = {
		PlayReq.REQ_FRIENDLY_TARGET: 0,
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_TARGET_TO_PLAY: 0}
	pass


class BOT_438:
	"""Cybertech Chip"""
	pass
