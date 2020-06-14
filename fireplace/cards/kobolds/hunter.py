from ..utils import *


##
# Minions

class LOOT_078:
	"""Cave Hydra"""
	pass


class LOOT_511:
	"""Kathrena Winterwisp"""
	pass


class LOOT_520:
	"""Seeping Oozeling"""
	pass


##
# Spells

class LOOT_077:
	"""Flanking Strike"""
	requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
	pass


class LOOT_079:
	"""Wandering Monster"""
	pass


class LOOT_080:
	"""Lesser Emerald Spellstone"""
	requirements = {PlayReq.REQ_MINION_TARGET: 0}
	pass


class LOOT_217:
	"""To My Side!"""
	requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_NUM_MINION_SLOTS: 1}
	pass


class LOOT_522:
	"""Crushing Walls"""
	pass


##
# Weapons

class LOOT_085:
	"""Rhok'delar"""
	pass


class LOOT_222:
	"""Candleshot"""
	pass
