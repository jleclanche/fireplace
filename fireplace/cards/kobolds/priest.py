from ..utils import *


##
# Minions

class LOOT_410:
	"""Duskbreaker"""
	requirements = {PlayReq.REQ_ENEMY_TARGET: 0, PlayReq.REQ_MINION_TARGET: 0}
	pass


class LOOT_528:
	"""Twilight Acolyte"""
	requirements = {
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_TARGET_IF_AVAILABLE_AND_DRAGON_IN_HAND: 0}
	pass


class LOOT_534:
	"""Gilded Gargoyle"""
	pass


class LOOT_538:
	"""Temporus"""
	pass


##
# Spells

class LOOT_008:
	"""Psychic Scream"""
	requirements = {PlayReq.REQ_ENEMY_TARGET: 0, PlayReq.REQ_MINION_TARGET: 0}
	pass


class LOOT_187:
	"""Twilight's Call"""
	requirements = {PlayReq.REQ_FRIENDLY_MINION_DIED_THIS_GAME: 0}
	pass


class LOOT_278:
	"""Unidentified Elixir"""
	requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
	pass


class LOOT_353:
	"""Psionic Probe"""
	pass


class LOOT_507:
	"""Lesser Diamond Spellstone"""
	pass


##
# Weapons

class LOOT_209:
	"""Dragon Soul"""
	pass
