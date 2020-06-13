from ..utils import *


##
# Minions

class GIL_130:
	"""Gloom Stag"""
	pass


class GIL_188:
	"""Druid of the Scythe"""
	pass


class GIL_507:
	"""Bewitched Guardian"""
	pass


class GIL_658:
	"""Splintergraft"""
	requirements = {
		PlayReq.REQ_FRIENDLY_TARGET: 0,
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
	pass


class GIL_800:
	"""Duskfallen Aviana"""
	pass


class GIL_833:
	"""Forest Guide"""
	pass


##
# Spells

class GIL_553:
	"""Wispering Woods"""
	pass


class GIL_571:
	"""Witching Hour"""
	requirements = {
		PlayReq.REQ_FRIENDLY_MINIONS_OF_RACE_DIED_THIS_GAME: 20,
		PlayReq.REQ_NUM_MINION_SLOTS: 1}
	pass


class GIL_637:
	"""Ferocious Howl"""
	requirements = {PlayReq.REQ_MINION_TARGET: 0}
	pass


class GIL_663:
	"""Witchwood Apple"""
	pass
