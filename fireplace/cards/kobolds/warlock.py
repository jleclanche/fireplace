from ..utils import *


##
# Minions

class LOOT_013:
	"""Vulgar Homunculus"""
	pass


class LOOT_014:
	"""Kobold Librarian"""
	pass


class LOOT_018:
	"""Hooked Reaver"""
	pass


class LOOT_306:
	"""Possessed Lackey"""
	pass


class LOOT_368:
	"""Voidlord"""
	pass


class LOOT_415:
	"""Rin, the First Disciple"""
	pass


##
# Spells

class LOOT_017:
	"""Dark Pact"""
	requirements = {
		PlayReq.REQ_FRIENDLY_TARGET: 0,
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_TARGET_TO_PLAY: 0}
	pass


class LOOT_043:
	"""Lesser Amethyst Spellstone"""
	requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
	pass


class LOOT_417:
	"""Cataclysm"""
	pass


##
# Weapons

class LOOT_420:
	"""Skull of the Man'ari"""
	pass
