from ..utils import *


##
# Minions

class GVG_074:
	"""Kezan Mystic"""
	play = Steal(RANDOM(ENEMY_SECRETS))


class GVG_089:
	"""Illuminator"""
	events = OWN_TURN_END.on(Find(FRIENDLY_SECRETS) & Heal(FRIENDLY_HERO, 4))


class GVG_094:
	"""Jeeves"""
	events = EndTurn().on(DrawUntil(EndTurn.PLAYER, 3))


class GVG_095:
	"""Goblin Sapper"""
	update = (Count(ENEMY_HAND) >= 6) & Refresh(SELF, {GameTag.ATK: +4})


class GVG_097:
	"""Lil' Exorcist"""
	# The Enchantment ID is correct
	play = Buff(SELF, "GVG_101e") * Count(ENEMY_MINIONS + DEATHRATTLE)


GVG_101e = buff(+1, +1)


class GVG_099:
	"""Bomb Lobber"""
	play = Hit(RANDOM_ENEMY_MINION, 4)
