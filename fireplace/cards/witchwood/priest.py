from ..utils import *


##
# Minions

class GIL_142:
	"""Chameleos"""
	pass


class GIL_156:
	"""Quartz Elemental"""
	pass


class GIL_190:
	"""Nightscale Matriarch"""
	pass


class GIL_805:
	"""Coffin Crasher"""
	pass


class GIL_835:
	"""Squashling"""
	requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
	pass


class GIL_837:
	"""Glitter Moth"""
	pass


class GIL_840:
	"""Lady in White"""
	pass


##
# Spells

class GIL_134:
	"""Holy Water"""
	requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
	pass


class GIL_661:
	"""Divine Hymn"""
	requirements = {PlayReq.REQ_FRIENDLY_TARGET: 0, PlayReq.REQ_MINION_TARGET: 0}
	pass


class GIL_813:
	"""Vivid Nightmare"""
	requirements = {
		PlayReq.REQ_FRIENDLY_TARGET: 0,
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_NUM_MINION_SLOTS: 1,
		PlayReq.REQ_TARGET_TO_PLAY: 0}
	pass
