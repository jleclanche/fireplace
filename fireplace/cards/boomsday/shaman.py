from ..utils import *


##
# Minions

class BOT_291:
	"""Storm Chaser"""
	pass


class BOT_407:
	"""Thunderhead"""
	pass


class BOT_411:
	"""Electra Stormsurge"""
	pass


class BOT_533:
	"""Menacing Nimbus"""
	pass


class BOT_543:
	"""Omega Mind"""
	pass


##
# Spells

class BOT_093:
	"""Elementary Reaction"""
	requirements = {PlayReq.REQ_FRIENDLY_TARGET: 0, PlayReq.REQ_TARGET_WITH_DEATHRATTLE: 0}
	pass


class BOT_099:
	"""Eureka!"""
	requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
	pass


class BOT_245:
	"""The Storm Bringer"""
	pass


class BOT_246:
	"""Beakered Lightning"""
	pass


class BOT_451:
	"""Voltaic Burst"""
	requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
	pass
