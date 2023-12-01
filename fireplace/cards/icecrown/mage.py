from ..utils import *


##
# Minions

class ICC_068:
	"""Ice Walker"""
	events = Activate(CONTROLLER, FRIENDLY_HERO_POWER).after(
		Find(Activate.TARGET) & Freeze(Activate.TARGET)
	)


class ICC_069:
	"""Ghastly Conjurer"""
	play = Give(CONTROLLER, "CS2_027")


class ICC_083:
	"""Doomed Apprentice"""
	update = Refresh(ENEMY_HAND + SPELL, {GameTag.COST: 1})


class ICC_252:
	"""Coldwraith"""
	play = Find(ENEMY + FROZEN) & Draw(CONTROLLER)


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
