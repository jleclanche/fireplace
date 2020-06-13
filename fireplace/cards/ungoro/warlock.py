from ..utils import *


##
# Minions

class UNG_047:
	"""Ravenous Pterrordax"""
	requirements = {
		PlayReq.REQ_FRIENDLY_TARGET: 0,
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
	pass


class UNG_049:
	"""Tar Lurker"""
	pass


class UNG_830:
	"""Cruel Dinomancer"""
	pass


class UNG_833:
	"""Lakkari Felhound"""
	pass


class UNG_835:
	"""Chittering Tunneler"""
	pass


class UNG_836:
	"""Clutchmother Zavas"""
	pass


##
# Spells

class UNG_829:
	"""Lakkari Sacrifice"""
	pass


class UNG_831:
	"""Corrupting Mist"""
	pass


class UNG_832:
	"""Bloodbloom"""
	pass


class UNG_834:
	"""Feeding Time"""
	requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
	pass
