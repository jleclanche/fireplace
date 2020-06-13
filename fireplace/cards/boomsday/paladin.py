from ..utils import *


##
# Minions

class BOT_236:
	"""Crystalsmith Kangor"""
	pass


class BOT_537:
	"""Mechano-Egg"""
	pass


class BOT_906:
	"""Glow-Tron"""
	pass


class BOT_910:
	"""Glowstone Technician"""
	pass


class BOT_911:
	"""Annoy-o-Module"""
	pass


##
# Spells

class BOT_234:
	"""Shrink Ray"""
	pass


class BOT_436:
	"""Prismatic Lens"""
	requirements = {PlayReq.REQ_FRIENDLY_TARGET: 0, PlayReq.REQ_MINION_TARGET: 0}
	pass


class BOT_908:
	"""Autodefense Matrix"""
	pass


class BOT_909:
	"""Crystology"""
	pass


class BOT_912:
	"""Kangor's Endless Army"""
	requirements = {
		PlayReq.REQ_FRIENDLY_MINIONS_OF_RACE_DIED_THIS_GAME: 17,
		PlayReq.REQ_NUM_MINION_SLOTS: 1}
	pass
