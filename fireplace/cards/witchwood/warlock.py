from ..utils import *


##
# Minions

class GIL_508:
	"""Duskbat"""
	pass


class GIL_515:
	"""Ratcatcher"""
	requirements = {
		PlayReq.REQ_FRIENDLY_TARGET: 0,
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
	pass


class GIL_565:
	"""Deathweb Spider"""
	pass


class GIL_608:
	"""Witchwood Imp"""
	pass


class GIL_618:
	"""Glinda Crowskin"""
	pass


class GIL_693:
	"""Blood Witch"""
	pass


class GIL_825:
	"""Lord Godfrey"""
	pass


##
# Spells

class GIL_191:
	"""Fiendish Circle"""
	pass


class GIL_543:
	"""Dark Possession"""
	requirements = {PlayReq.REQ_FRIENDLY_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
	pass


class GIL_665:
	"""Curse of Weakness"""
	pass
