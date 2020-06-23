from ..utils import *


##
# Minions

class GIL_128:
	"""Emeriss"""
	pass


class GIL_200:
	"""Duskhaven Hunter"""
	pass


class GIL_562:
	"""Vilebrood Skitterer"""
	pass


class GIL_607:
	"""Toxmonger"""
	pass


class GIL_607t:
	"""Hunting Mastiff"""
	pass


class GIL_650:
	"""Houndmaster Shaw"""
	pass


class GIL_905:
	"""Carrion Drake"""
	pass


##
# Spells

class GIL_518:
	"""Wing Blast"""
	requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
	pass


class GIL_577:
	"""Rat Trap"""
	pass


class GIL_828:
	"""Dire Frenzy"""
	requirements = {
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_TARGET_TO_PLAY: 0,
		PlayReq.REQ_TARGET_WITH_RACE: 20}
	pass
