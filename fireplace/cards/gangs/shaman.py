from ..utils import *


##
# Minions

class CFM_061:
	"""Jinyu Waterspeaker"""
	pass


class CFM_312:
	"""Jade Chieftain"""
	play = SummonJadeGolem(CONTROLLER).then(Taunt(SummonJadeGolem.CARD))


class CFM_324:
	"""White Eyes"""
	pass


class CFM_697:
	"""Lotus Illusionist"""
	pass


##
# Spells

class CFM_310:
	"""Call in the Finishers"""
	pass


class CFM_313:
	"""Finders Keepers"""
	pass


class CFM_696:
	"""Devolve"""
	pass


class CFM_707:
	"""Jade Lightning"""
	play = Hit(TARGET, 4), SummonJadeGolem(CONTROLLER)


##
# Weapons

class CFM_717:
	"""Jade Claws"""
	play = SummonJadeGolem(CONTROLLER)
