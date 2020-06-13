from ..utils import *


##
# Minions

class ICC_068:
	"""Ice Walker"""
	pass


class ICC_069:
	"""Ghastly Conjurer"""
	pass


class ICC_083:
	"""Doomed Apprentice"""
	pass


class ICC_252:
	"""Coldwraith"""
	requirements = {PlayReq.REQ_FROZEN_TARGET: 0, PlayReq.REQ_MINION_TARGET: 0}
	pass


class ICC_838:
	"""Sindragosa"""
	pass


##
# Spells

class ICC_082:
	"""Frozen Clone"""
	pass


class ICC_086:
	"""Glacial Mysteries"""
	requirements = {PlayReq.REQ_SECRET_ZONE_CAP_FOR_NON_SECRET: 0}
	pass


class ICC_823:
	"""Simulacrum"""
	pass


class ICC_836:
	"""Breath of Sindragosa"""
	requirements = {PlayReq.REQ_MINIMUM_ENEMY_MINIONS: 1}
	pass


##
# Heros

class ICC_833:
	"""Frost Lich Jaina"""
	pass
