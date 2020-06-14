from ..utils import *


##
# Minions

class LOOT_111:
	"""Scorp-o-matic"""
	requirements = {
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
		PlayReq.REQ_TARGET_MAX_ATTACK: 1}
	pass


class LOOT_118:
	"""Ebon Dragonsmith"""
	pass


class LOOT_124:
	"""Lone Champion"""
	pass


class LOOT_150:
	"""Furbolg Mossbinder"""
	requirements = {
		PlayReq.REQ_FRIENDLY_TARGET: 0,
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
	pass


class LOOT_154:
	"""Gravelsnout Knight"""
	pass


class LOOT_218:
	"""Feral Gibberer"""
	pass


class LOOT_382:
	"""Kobold Monk"""
	pass


class LOOT_383:
	"""Hungry Ettin"""
	pass


class LOOT_394:
	"""Shrieking Shroom"""
	pass
