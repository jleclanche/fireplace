from ..utils import *


##
# Minions

class CFM_342:
	"""Luckydo Buccaneer"""
	pass


class CFM_634:
	"""Lotus Assassin"""
	pass


class CFM_636:
	"""Shadow Rager"""
	pass


class CFM_691:
	"""Jade Swarmer"""
	deathrattle = SummonJadeGolem(CONTROLLER)


class CFM_693:
	"""Gadgetzan Ferryman"""
	pass


class CFM_694:
	"""Shadow Sensei"""
	pass


class CFM_781:
	"""Shaku, the Collector"""
	pass


##
# Spells

class CFM_630:
	"""Counterfeit Coin"""
	pass


class CFM_690:
	"""Jade Shuriken"""
	play = Hit(TARGET, 2)
	combo = Hit(TARGET, 2), SummonJadeGolem(CONTROLLER)
