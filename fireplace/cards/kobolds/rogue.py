from ..utils import *


##
# Minions

class LOOT_026:
	"""Fal'dorei Strider"""
	pass


class LOOT_033:
	"""Cavern Shinyfinder"""
	pass


class LOOT_165:
	"""Sonya Shadowdancer"""
	pass


class LOOT_211:
	"""Elven Minstrel"""
	requirements = {PlayReq.REQ_FRIENDLY_TARGET: 0, PlayReq.REQ_MINION_TARGET: 0}
	pass


class LOOT_412:
	"""Kobold Illusionist"""
	pass


##
# Spells

class LOOT_204:
	"""Cheat Death"""
	pass


class LOOT_210:
	"""Sudden Betrayal"""
	pass


class LOOT_214:
	"""Evasion"""
	pass


class LOOT_503:
	"""Lesser Onyx Spellstone"""
	requirements = {PlayReq.REQ_MINIMUM_ENEMY_MINIONS: 1}
	pass


##
# Weapons

class LOOT_542:
	"""Kingsbane"""
	pass
